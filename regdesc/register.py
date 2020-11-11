import collections
from . import utils


class FieldDescriptor:
    def __init__(self, shift, width, reset_value):
        self.shift = int(shift)
        self.width = int(width)
        self.reset_value = int(reset_value)
        self.mask = ((1 << self.width) - 1) << self.shift

    def __get__(self, reg, owner):
        if reg is None:
            return self

        return (reg.storage & self.mask) >> self.shift

    def __set__(self, reg, value):
        assert value.bit_length() <= self.width

        reg.storage = (reg.storage & ~self.mask) | ((value << self.shift) & self.mask)


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
        dct["reset_value"] = 0
        attrs = []

        for key, attr in dct.items():
            if isinstance(attr, Field):
                attrs.append((key, attr))
                dct[key] = FieldDescriptor(shift, attr.width, attr.value)
                dct["reset_value"] += attr.value << shift
                shift += attr.width

        dct["_fields"] = collections.OrderedDict(attrs)
        dct["width"] = shift

        return type.__new__(cls, name, bases, dct)


class Register(metaclass=RegisterMeta):
    def __init__(self, *, reset_value=None, **kwds):
        # override default reset value
        if reset_value is not None:
            reset_value = int(reset_value)
            if reset_value.bit_length() >= self.width:
                raise ValueError("reset_value too long")
            self.reset_value = reset_value

        self.storage = self.reset_value

        # override default field values with passed keywords
        for name, value in kwds.items():
            setattr(self, name, value)

    def __str__(self):
        return utils.bin(self.storage, self.width)

    def __int__(self):
        return self.storage

    @property
    def fields(self):
        return collections.OrderedDict(
            [
                (field.name, hex(getattr(self, key)))
                for key, field in self._fields.items()
            ]
        )
