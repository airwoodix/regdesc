import unittest
from regdesc.devices import adf4002

_regnames = ["InitLatch", "FunctionLatch", "NCounterLatch", "RCounterLatch"]
_regs = {name: getattr(adf4002, name) for name in _regnames}


class TestRegisterDescription(unittest.TestCase):
    def test_reg_width(self):
        for name, reg in _regs.items():
            self.assertEqual(reg.__width__, 24, name)

    def test_cb_readonly(self):
        for name, reg in _regs.items():
            self.assertTrue(reg.control_bits._field.readonly, name)

    def test_cb_width(self):
        for name, reg in _regs.items():
            self.assertEqual(reg.control_bits._field.width, 2, name)

    def test_cb_reset(self):
        self.assertEqual(adf4002.InitLatch.control_bits._field.reset, 3)
        self.assertEqual(adf4002.FunctionLatch.control_bits._field.reset, 2)
        self.assertEqual(adf4002.NCounterLatch.control_bits._field.reset, 1)
        self.assertEqual(adf4002.RCounterLatch.control_bits._field.reset, 0)


class TestDevice(unittest.TestCase):
    def test_instantiate(self):
        adf4002.ADF4002()
