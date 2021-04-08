from dataclasses import dataclass, field as dataclass_field
from typing import Optional, Dict, Any

__all__ = ["Field", "Register", "unsafe"]


@dataclass
class unsafe:
    """
    A tag for unsafe literal values passed where variants are expected.

    ```
    class Reg(Register):
        __address__ = 1

        f0 = Field(1, variants={"enable": 1, "disable": 0})

    reg = Reg()
    reg.f0 = "enable"  # valid
    reg.f0 = 1  # invalid
    reg.f0 = unsafe(1)  # valid
    ```
    """

    value: int

    def __int__(self):
        return self.value


class FieldDescriptor:
    def __init__(self, field):
        self._field = field

    def __get__(self, reg, owner):
        if reg is None:
            return self

        value = (reg.value >> self._field.shift) & self._field.mask
        return self._field._rev_resolve(value)

    def __set__(self, reg, value):
        if self._field.readonly:
            raise NotImplementedError("read only field")

        value = self._field._resolve(value)
        _check_value(value, self._field.width)

        reg.value = (reg.value & ~(self._field.mask << self._field.shift)) | (
            (value & self._field.mask) << self._field.shift
        )


@dataclass
class Field:
    """
    A bit field in a register
    """

    width: int = 1
    reset: Any = unsafe(0)
    readonly: bool = False
    doc: Optional[str] = None
    variants: Optional[Dict[Any, int]] = None

    mask: int = dataclass_field(init=False)
    shift: int = dataclass_field(init=False)
    rev_variants: Optional[Dict[int, Any]] = None

    def __post_init__(self):
        object.__setattr__(self, "width", int(self.width))
        if self.width < 1:
            raise ValueError("width < 1")

        if self.variants is not None:
            for value in self.variants.values():
                _check_value(value, self.width)

            # explictly reject aliases
            if len(self.variants) > len(set(self.variants.values())):
                raise ValueError("Variant values must be unique")

            # build reverse map
            object.__setattr__(
                self, "rev_variants", {v: k for k, v in self.variants.items()}
            )

        object.__setattr__(self, "reset", self._resolve(self.reset))
        _check_value(self.reset, self.width, "reset")

    def _resolve(self, value):
        if not isinstance(value, unsafe) and self.variants is not None:
            return int(self.variants[value])

        return int(value)

    def _rev_resolve(self, value):
        if self.rev_variants is not None:
            return self.rev_variants[value]

        return int(value)


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
            _check_value(reset, self.__width__)
            self.__reset__ = reset

        self.value = self.__reset__

        for name, value in kwds.items():
            setattr(self, name, value)

    def __int__(self):
        return self.value

    def fields(self, *, show_reserved=False, output="hex"):
        """
        Return a dict of evaluated values of the register's fields.

        `show_reserved`: if `True`, also include underscore-prefixed fields
        `output`: determines the value format. One of:
            - `"hex"`: hexadecimal string
            - `"variant"`: if available, the corresponding variant,
              else a (decimal) integer
            - `"dec"`: (decimal) integer.
        """
        assert output in ["hex", "dec", "variant"]

        def process_value(v, field):
            if output == "hex":
                return hex(field._resolve(v))
            elif output == "variant":
                return v
            else:
                return int(field._resolve(v))

        return {
            key: process_value(getattr(self, key), field)
            for key, field in self.__register_fields__.items()
            if show_reserved or not key.startswith("_")
        }


def _check_value(value, width, name="value"):
    if value.bit_length() > width:
        raise ValueError(f"{name} too large")
    if value < 0:
        raise ValueError(f"negative {name}")
