from dataclasses import dataclass, field as dataclass_field
from typing import Optional

__all__ = ["Field", "Register"]


class FieldDescriptor:
    def __init__(self, field):
        self._field = field

    def __get__(self, reg, owner):
        if reg is None:
            return self

        return (reg.value >> self._field.shift) & self._field.mask

    def __set__(self, reg, value):
        if self._field.readonly:
            raise NotImplementedError("read only field")

        _check_size(value, self._field.width)

        reg.value = (reg.value & ~(self._field.mask << self._field.shift)) | (
            (value & self._field.mask) << self._field.shift
        )


@dataclass
class Field:
    """
    A bit field in a register
    """

    width: int = 1
    reset: int = 0
    readonly: bool = False
    doc: Optional[str] = None

    mask: int = dataclass_field(init=False)
    shift: int = dataclass_field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "width", int(self.width))
        if self.width < 1:
            raise ValueError("width < 1")

        object.__setattr__(self, "reset", int(self.reset))
        if self.reset.bit_length() > self.width:
            raise ValueError("reset value too large")
        elif self.reset < 0:
            raise ValueError("negative reset")


class RegisterMeta(type):
    def __new__(cls, cls_name, bases, dct):
        shift = 0
        reg_reset = 0
        fields = {}

        for name, field in dct.items():
            if isinstance(field, Field):
                field.mask = (1 << field.width) - 1
                field.shift = shift
                dct[name] = FieldDescriptor(field)
                fields[name] = field

                reg_reset |= field.reset << shift
                shift += field.width

        if cls_name != "Register":
            if "__address__" not in dct:
                if "control_bits" in fields:
                    assert fields["control_bits"].readonly
                    dct["__address__"] = fields["control_bits"].reset
                elif "address" in fields:
                    assert fields["address"].readonly
                    dct["__address__"] = fields["address"].reset
                else:
                    raise ValueError("missing address")

        dct["__register_fields__"] = fields
        dct["__width__"] = shift
        dct["__reset__"] = reg_reset

        return type.__new__(cls, name, bases, dct)


class Register(metaclass=RegisterMeta):
    """
    A hardware register
    """

    def __init__(self, *, reset=None, **kwds):
        if reset is not None:
            reset = int(reset)
            _check_size(reset, self.__width__)
            self.__reset__ = reset

        self.value = self.__reset__

        for name, value in kwds.items():
            setattr(self, name, value)

    def __int__(self):
        return self.value

    def fields(self, *, show_reserved=False, hex_values=True):
        process_value = hex if hex_values else int

        return {
            key: process_value(getattr(self, key))
            for key in self.__register_fields__.keys()
            if show_reserved or not key.startswith("_")
        }


def _check_size(value, width):
    if value.bit_length() > width:
        raise ValueError("value too large")
