"""
AD5781 True 18-Bit, Voltage Output DAC
https://www.analog.com/en/products/ad5781.html
"""

from ..register import Field, Register


class DacRegister(Register):
    _reserved = Field(2, readonly=True)
    data = Field(18, doc="18-bits DAC data")
    address = Field(3, reset=1, readonly=True, doc="Register address")
    rw = Field(doc="read/~write")


class ControlRegister(Register):
    _reserved0 = Field(readonly=True)
    rbuf = Field(reset=1, doc="Output amplifier configuration control")
    opgnd = Field(reset=1, doc="Output ground clamp control")
    dactri = Field(reset=1, doc="DAC tristate control")
    bin_2sc = Field(doc="DAC register coding select")
    sdodis = Field(doc="SDO pin enable/disable control")
    lin_comp = Field(4, doc="Linearity error compensation")
    _reserved1 = Field(10, readonly=True)
    address = Field(3, reset=2, readonly=True, doc="Register address")
    rw = Field(doc="read/~write")


class ClearcodeRegister(Register):
    _reserved = Field(2, readonly=True)
    data = Field(18, doc="18-bits data")
    address = Field(3, reset=3, readonly=True, doc="Register address")
    rw = Field(doc="read/~write")


class SoftwareControlRegister(Register):
    ldac = Field(doc="DAC register update")
    clr = Field(doc="Clear DAC register")
    reset = Field(doc="Reset to power-on state")
    _reserved = Field(17, readonly=True)
    address = Field(3, reset=4, readonly=True, doc="Register address")
    rw = Field(doc="read/~write")
