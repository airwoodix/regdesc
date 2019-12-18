import collections
from . import utils


class FieldDescriptor:
    def __init__(self, shift, width):
        self.shift = int(shift)
        self.width = int(width)
        self.mask = ((1 << self.width) - 1) << self.shift

    def __get__(self, reg, owner):
        if reg is None:
            return self

        return (reg.storage & self.mask) >> self.shift

    def __set__(self, reg, value):
        assert value.bit_length() <= self.width

        reg.storage = (reg.storage & ~self.mask) | \
          ((value << self.shift) & self.mask)


class Field:
    def __init__(self, name, *, width, value=0):
        self.name = name.upper()
        self.width = int(width)
        self.value = int(value)

        assert self.width > 0
        assert self.value.bit_length() <= self.width


class RegisterMeta(type):
    @classmethod
    def __prepare__(cls, name, bases):
        return collections.OrderedDict()

    def __new__(cls, name, bases, dct):
        # iterate through class attributes and transform
        # `Field` instances into corresponding descriptors
        shift = 0
        dct["initial_value"] = 0
        attrs = []

        for key, attr in dct.items():
            if isinstance(attr, Field):
                attrs.append((key, attr))
                dct[key] = FieldDescriptor(shift, attr.width)
                dct["initial_value"] += attr.value << shift
                shift += attr.width
                
        dct["_fields"] = collections.OrderedDict(attrs)
        dct["width"] = shift

        return type.__new__(cls, name, bases, dct)


class Register(metaclass=RegisterMeta):
    def __init__(self, *, initial_value=None, **kwds):
        # override default initial value
        if initial_value is not None:
            initial_value = int(initial_value)
            if initial_value.bit_length() >= self.width:
                raise ValueError("initial_value too long")
            self.initial_value = initial_value

        self.storage = self.initial_value

        # override default field values with passed keywords
        for name, value in kwds.items():
            setattr(self, name, value)

    def __str__(self):
        return utils.bin(self.storage, self.width)

    def __int__(self):
        return self.storage

    @property
    def fields(self):
        return collections.OrderedDict([
            (field.name, hex(getattr(self, key)))
            for key, field in self._fields.items()])
