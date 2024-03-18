import inspect
from ..utils import get_object_registers, camel_to_snake


def device(cls=None, /, *, obj=None, regs=None):
    """
    Fill a class with Register objects.

    :param `obj`: object to inspect to find register definitions.
    :param `regs`: register definitions as dict {name: reg_class}.

    Register definitions are searched for in the following order.
    The first non-empty set is used.
        1. ``regs`` (as-is)
        2. ``obj``
        3. the decorated class
        4. the caller's module
    """
    caller_frame = inspect.stack()[1]
    caller_module = inspect.getmodule(caller_frame[0])

    def wrap(cls):
        return _process_class(cls, obj, caller_module, regs)

    if cls is None:
        return wrap

    return wrap(cls)


def _process_class(cls, obj, mod, regs):
    regs = (
        regs or get_object_registers(obj) or get_object_registers(cls) or get_object_registers(mod)
    )

    setattr(cls, "_regs", regs)
    setattr(cls, "__init__", _device_init)  # FIXME: don't override existing __init__

    return cls


def _device_init(self):
    # address-indexed registers
    self.regs = {reg.__address__: reg() for reg in self._regs.values()}

    # named proxies
    for addr, name in zip(self.regs.keys(), self._regs.keys()):
        setattr(self, camel_to_snake(name), self.regs[addr])
