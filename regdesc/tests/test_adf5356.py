import unittest
from regdesc.devices import adf5356

_regnames = [f"R{n}" for n in range(14)]
_regs = [getattr(adf5356, name) for name in _regnames]


class TestRegisterDescription(unittest.TestCase):
    def test_reg_width(self):
        for reg in _regs:
            self.assertEqual(reg.__width__, 32, reg.__name__)

    def test_cb_readonly(self):
        for reg in _regs:
            self.assertTrue(reg.control_bits._field.readonly, reg.__name__)

    def test_cb_width(self):
        for reg in _regs:
            self.assertEqual(reg.control_bits._field.width, 4, reg.__name__)

    def test_cb_reset(self):
        for reset, reg in enumerate(_regs):
            self.assertEqual(reg.control_bits._field.reset, reset, reg.__name__)


class TestDevice(unittest.TestCase):
    def test_instantiate(self):
        adf5356.ADF5356()
