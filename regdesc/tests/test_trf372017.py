import unittest
from regdesc.devices import trf372017

_regnames = [f"R{n}" for n in range(1, 8)]
_regs = [getattr(trf372017, name) for name in _regnames]


class TestRegisterDescription(unittest.TestCase):
    def test_reg_width(self):
        for reg in _regs:
            self.assertEqual(reg.__width__, 32, reg.__name__)

    def test_address_readonly(self):
        for reg in _regs:
            self.assertTrue(reg.address._field.readonly, reg.__name__)

    def test_address_width(self):
        for reg in _regs:
            self.assertEqual(reg.address._field.width, 5, reg.__name__)

    def test_address_reset(self):
        for num, reg in enumerate(_regs):
            self.assertEqual(reg.address._field.reset, num + 9, reg.__name__)


class TestDevice(unittest.TestCase):
    def test_instantiate(self):
        trf372017.TRF372017()

    def test_integer_mode_example(self):
        # Datasheet §7.3.2.2
        dev = trf372017.TRF372017()

        f_ref = 40e6
        dev.r2.pll_div_sel = 1
        dev.r1.rdiv = 20
        dev.r2.nint = 800
        dev.r6.lo_div_sel = 1

        self.assertEqual(dev.f_pfd(f_ref), 2e6)
        self.assertEqual(dev.f_vco(f_ref), 3200e6)
        self.assertEqual(dev.f_lo(f_ref), 1600e6)
