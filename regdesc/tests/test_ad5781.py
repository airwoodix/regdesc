import inspect
import unittest

from regdesc import Register
from regdesc.devices import ad5781


def is_register(obj):
    return inspect.isclass(obj) and issubclass(obj, Register) and obj is not Register

_regs = {name: obj for name, obj in inspect.getmembers(ad5781, is_register)}


class TestRegisterDescription(unittest.TestCase):
    def test_register_width(self):
        for name, reg in _regs.items():
            self.assertEqual(reg.__width__, 24, name)

    def test_address_readonly(self):
        for name, reg in _regs.items():
            self.assertTrue(reg.address._field.readonly, name)

    def test_address_width(self):
        for name, reg in _regs.items():
            self.assertEqual(reg.address._field.width, 3, name)

    def test_address_reset(self):
        self.assertEqual(ad5781.DacRegister.address._field.reset, 1)
        self.assertEqual(ad5781.ControlRegister.address._field.reset, 2)
        self.assertEqual(ad5781.ClearcodeRegister.address._field.reset, 3)
        self.assertEqual(ad5781.SoftwareControlRegister.address._field.reset, 4)
