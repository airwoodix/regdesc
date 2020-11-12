import unittest
from regdesc.devices import adf4360_8

_regnames = ["ControlLatch", "NCounterLatch", "RCounterLatch"]
_regs = [getattr(adf4360_8, name) for name in _regnames]


class TestRegisterDescription(unittest.TestCase):
    def test_reg_width(self):
        for reg in _regs:
            self.assertEqual(reg.__width__, 24, reg.__name__)

    def test_cb_readonly(self):
        for reg in _regs:
            self.assertTrue(reg.control_bits._field.readonly, reg.__name__)

    def test_cb_width(self):
        for reg in _regs:
            self.assertEqual(reg.control_bits._field.width, 2, reg.__name__)

    def test_cb_reset(self):
        self.assertEqual(adf4360_8.ControlLatch.control_bits._field.reset, 0)
        self.assertEqual(adf4360_8.NCounterLatch.control_bits._field.reset, 2)
        self.assertEqual(adf4360_8.RCounterLatch.control_bits._field.reset, 1)


class TestDevice(unittest.TestCase):
    def test_instantiate(self):
        adf4360_8.ADF4360_8()
