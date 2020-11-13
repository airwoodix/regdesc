import inspect
from ..utils import get_object_registers, camel_to_snake


def device(cls=None, /, *, obj=None, regs=None):
    """
    Fill a class with Register objects.

    :param `obj`: object to inspect to find register definitions.
    :param `regs`: register definitions as dict {name: reg_class} (overrides those maybe found in ``obj``)

    If both ``obj`` and ``regs`` are ``None``, ``obj`` defaults to the caller's module.
    If ``obj`` doesn't contain any register definitions, ``cls`` is searched for some.
    """
    if obj is None and regs is None:
        caller_frame = inspect.stack()[1]
        obj = inspect.getmodule(caller_frame[0])

    def wrap(cls):
        return _process_class(cls, obj, regs)

    if cls is None:
        return wrap

    return wrap(cls)


def _process_class(cls, obj, regs):
    if regs is None:
        if obj is not None:
            regs = get_object_registers(obj)

        if not regs:
            regs = get_object_registers(cls)

    setattr(cls, "_regs", regs)
    setattr(cls, "__init__", _device_init)  # FIXME: don't override existing __init__

    return cls


def _device_init(self):
    # address-indexed registers
    self.regs = {reg.__address__: reg() for reg in self._regs.values()}

    # named proxies
    for addr, name in zip(self.regs.keys(), self._regs.keys()):
        setattr(self, camel_to_snake(name), self.regs[addr])
