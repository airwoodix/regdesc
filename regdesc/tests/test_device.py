import unittest
from regdesc import Register, Field, device


class Reg0(Register):
    __address__ = 0

    f0 = Field(3, reset=2)
    f1 = Field(2, reset=1, readonly=True)


class Reg12(Register):
    __address__ = 12

    f0 = Field()


@device(regs=dict(reg0=Reg0))
class RegDevice:
    pass


@device
class ModDevice:
    pass


class TestDevice(unittest.TestCase):
    def setUp(self):
        self.reg_dev = RegDevice()
        self.mod_dev = ModDevice()
        self.mod_dev2 = ModDevice()

    def test_decorator_regs(self):
        self.assertEqual(len(self.reg_dev.regs), 1)

    def test_decorator_mod(self):
        self.assertEqual(len(self.mod_dev.regs), 2)

    def test_access_by_address(self):
        self.assertIsInstance(self.mod_dev.regs[0], Reg0)
        self.assertIsInstance(self.mod_dev.regs[12], Reg12)

        with self.assertRaises(KeyError):
            self.mod_dev.regs[1]

    def test_named_proxy(self):
        self.assertIsInstance(self.mod_dev.reg0, Reg0)
        self.assertIsInstance(self.mod_dev.reg12, Reg12)

    def test_mod_field(self):
        self.assertEqual(self.mod_dev.regs[0].f0, 2)  # reset value
        self.mod_dev.reg0.f0 = 3
        self.assertEqual(self.mod_dev.regs[0].f0, 3)

        self.assertEqual(self.mod_dev.reg12.f0, 0)
        self.mod_dev.regs[12].f0 = 1
        self.assertEqual(self.mod_dev.reg12.f0, 1)

    def test_instance_attributes(self):
        self.assertEqual(self.mod_dev.reg0.f0, 2)
        self.assertEqual(self.mod_dev2.reg0.f0, 2)

        self.mod_dev.reg0.f0 = 3
        self.assertEqual(self.mod_dev.reg0.f0, 3)
        self.assertEqual(self.mod_dev2.reg0.f0, 2)

    def test_readonly(self):
        with self.assertRaises(NotImplementedError):
            self.mod_dev.reg0.f1 = 0
