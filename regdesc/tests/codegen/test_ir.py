import io
import json
import unittest
import sys

from regdesc.codegen import ir
from regdesc import Register, Field


class TestJSONWriter(unittest.TestCase):
    def test_invalid_device(self):
        with self.assertRaises(ValueError):
            buf = io.StringIO()
            ir.emit_json("non_existing_device", buf)

    def test_valid_json(self):
        buf = io.StringIO()
        ir.emit_json("ad9910", buf)
        buf.seek(0)
        json.load(buf)


class Reg0(Register):
    __address__ = 0

    f0 = Field(3, reset=2, doc="f0")
    f1 = Field(readonly=True, reset=1)
    f2 = Field(16)


class Reg1(Register):
    __address__ = 1

    f0 = Field()
    _f1 = Field(3, readonly=True)
    f2 = Field(2, reset=1)


def find_by_name(name, d):
    return [x for x in d if x["name"] == name][0]


class TestDictSerializer(unittest.TestCase):
    def setUp(self):
        self.d = ir.serialize(sys.modules[__name__])

    def test_load_device(self):
        d = ir.serialize("ad9910")
        self.assertIsInstance(d, dict)

    def test_load_module(self):
        self.assertIsInstance(self.d, dict)

    def test_skip_reserved(self):
        d = ir.serialize(sys.modules[__name__], keep_reserved_fields=False)
        self.assertIsInstance(d, dict)

        reg = find_by_name("Reg1", d["registers"])
        with self.assertRaises(IndexError):
            find_by_name("_f1", reg["fields"])

    def test_all_regs_present(self):
        find_by_name("Reg0", self.d["registers"])
        find_by_name("Reg1", self.d["registers"])

        # sanity check
        with self.assertRaises(IndexError):
            find_by_name("INVALID", self.d["registers"])

    def test_field_attrs(self):
        reg = find_by_name("Reg0", self.d["registers"])

        f0 = find_by_name("f0", reg["fields"])
        self.assertEqual(f0["width"], 3)
        self.assertEqual(f0["reset"], 2)
        self.assertFalse(f0["readonly"])
        self.assertEqual(f0["doc"], "f0")
        self.assertEqual(f0["shift"], 0)
        self.assertEqual(f0["mask"], 0x7)

        f1 = find_by_name("f1", reg["fields"])
        self.assertEqual(f1["width"], 1)
        self.assertEqual(f1["reset"], 1)
        self.assertTrue(f1["readonly"])
        self.assertEqual(f1["doc"], None)
        self.assertEqual(f1["shift"], 3)
        self.assertEqual(f1["mask"], 0x1)

        f2 = find_by_name("f2", reg["fields"])
        self.assertEqual(f2["width"], 16)
        self.assertEqual(f2["reset"], 0)
        self.assertFalse(f2["readonly"])
        self.assertEqual(f2["doc"], None)
        self.assertEqual(f2["shift"], 4)
        self.assertEqual(f2["mask"], 0xFFFF)

    def test_reg_attrs(self):
        reg = find_by_name("Reg0", self.d["registers"])

        self.assertEqual(reg["address"], 0)
        self.assertEqual(reg["width"], 20)
        self.assertEqual(reg["reset"], (1 << 3) | 2)

    def test_top_level_attrs(self):
        self.assertEqual(self.d["device"], __name__.split(".")[-1])
        d = ir.serialize("ad9910")
        self.assertEqual(d["device"], "ad9910")
