import inspect
from ..utils import get_object_registers, camel_to_snake
from ..register import Register


def device(cls=None, /, *, mod=None, regs=None):
    """
    Fill a class with Register objects.

    :param `mod`: module to inspect to find register definitions. If ``None``, the caller's module except if ``regs`` is given.
    :param `regs`: register definitions as dict {name: reg_class}
    """
    if mod is None and regs is None:
        caller_frame = inspect.stack()[1]
        mod = inspect.getmodule(caller_frame[0])

    def wrap(cls):
        return _process_class(cls, mod, regs)

    if cls is None:
        return wrap

    return wrap(cls)


def _process_class(cls, mod, regs):
    if regs is None:
        regs = {}

    if mod is not None:
        regs = get_object_registers(mod)

    setattr(cls, "_regs", regs)
    setattr(cls, "__init__", _device_init)  # FIXME: don't override existing __init__

    return cls


def _device_init(self):
    # address-indexed registers
    self.regs = {reg.__address__: reg() for reg in self._regs.values()}

    # named proxies
    for addr, name in zip(self.regs.keys(), self._regs.keys()):
        setattr(self, camel_to_snake(name), self.regs[addr])
