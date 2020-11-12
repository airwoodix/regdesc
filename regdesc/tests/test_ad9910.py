import unittest
from regdesc.devices import ad9910


class TestRegisterDescription(unittest.TestCase):
    def _assert_width_equals(self, names, width):
        for name in names:
            reg = getattr(ad9910, name)
            self.assertEqual(reg.__width__, width, name)

    def test_16b_registers(self):
        names = ["POW"]
        self._assert_width_equals(names, 16)

    def test_32b_registers(self):
        names = [
            "CFR1",
            "CFR2",
            "CFR3",
            "AuxDACControl",
            "IOUpdateRate",
            "FTW",
            "ASF",
            "MultichipSync",
            "DigitalRampRate",
        ]
        self._assert_width_equals(names, 32)

    def test_64b_registers(self):
        names = (
            ["DigitalRampLimit", "DigitalRampStepSize"]
            + [f"SingleToneProfile{n}" for n in range(8)]
            + [f"RAMProfile{n}" for n in range(8)]
        )
        self._assert_width_equals(names, 64)

    def test_reset_values(self):
        data = (
            [
                ("CFR1", 0),
                ("CFR2", 0x400820),
                ("CFR3", 0x1F3F4000),
                ("AuxDACControl", 0x7F),
                ("IOUpdateRate", 0xFFFFFFFF),
                ("FTW", 0),
                ("POW", 0),
                ("ASF", 0),
                ("MultichipSync", 0),
                ("SingleToneProfile0", 0x08B5000000000000),
            ]
            + [(f"SingleToneProfile{n}", 0) for n in range(1, 8)]
            + [(f"RAMProfile{n}", 0) for n in range(0, 8)]
        )

        for name, reset in data:
            reg = getattr(ad9910, name)
            self.assertEqual(reg.__reset__, reset, name)


class TestDevice(unittest.TestCase):
    def test_instantiate(self):
        ad9910.AD9910()
