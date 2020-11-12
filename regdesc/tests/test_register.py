import unittest
from regdesc import Field, Register


class TestRegAddrInReg(Register):
    address = Field(2, reset=2, readonly=True)
    f0 = Field(12, reset=12)


class TestRegCBInReg(Register):
    control_bits = Field(3, reset=5, readonly=True)
    f0 = Field(12, reset=12)
    f1 = Field(14, reset=1234)


class TestReg(Register):
    __address__ = 0xE

    f0 = Field(12, reset=12)
    f1 = Field(14, reset=1234)
    f2 = Field(2)
    _reserved0 = Field(readonly=True)
    f3 = Field(15)


class TestRegister(unittest.TestCase):
    def setUp(self):
        self.reg_addr = TestRegAddrInReg()
        self.reg_cb = TestRegCBInReg()
        self.reg = TestReg()

    def test_address(self):
        self.assertEqual(self.reg.__address__, 0xE)
        self.assertEqual(self.reg_cb.__address__, 5)
        self.assertEqual(self.reg_addr.__address__, 2)

    def test_reg_width(self):
        self.assertEqual(self.reg.__width__, 12 + 14 + 2 + 1 + 15)
        self.assertEqual(self.reg_cb.__width__, 3 + 12 + 14)
        self.assertEqual(self.reg_addr.__width__, 2 + 12)

    def test_reg_reset(self):
        self.assertEqual(self.reg.__reset__, (1234 << 12) | 12)
        self.assertEqual(self.reg_cb.__reset__, (1234 << 15) | (12 << 3) | 5)
        self.assertEqual(self.reg_addr.__reset__, (12 << 2) | 2)

    def test_immutable_fields(self):
        with self.assertRaises(NotImplementedError):
            self.reg_addr.address = 1

        with self.assertRaises(NotImplementedError):
            self.reg_cb.control_bits = 4

    def test_read_field(self):
        self.assertEqual(self.reg.f0, 12)
        self.assertEqual(self.reg.f1, 1234)
        self.assertEqual(self.reg.f2, 0)

    def test_set_field(self):
        self.reg.f0 = 123
        self.assertEqual(self.reg.f0, 123)

        self.reg.f1 = 42
        self.assertEqual(self.reg.f1, 42)

    def test_field_dict(self):
        self.assertIsInstance(self.reg.fields(), dict)

    def test_reg_value(self):
        self.assertEqual(self.reg.__reset__, self.reg.value)
        self.assertEqual(self.reg_addr.__reset__, self.reg_addr.value)
        self.assertEqual(self.reg_cb.__reset__, self.reg_cb.value)

    def test_reg_set_field_value(self):
        self.assertEqual(self.reg.value, 12 | (1234 << 12))
        self.reg.f1 = 2345
        self.assertEqual(self.reg.value, 12 | (2345 << 12))

    def test_field_strip_reserved(self):
        self.assertNotIn("_reserved0", self.reg.fields())
        self.assertIn("_reserved0", self.reg.fields(show_reserved=True))

    def test_field_process_values(self):
        for val in self.reg.fields().values():
            self.assertIsInstance(val, str)
            self.assertTrue(val.lower().startswith("0x"))

        for val in self.reg.fields(hex_values=False).values():
            self.assertIsInstance(val, int)
