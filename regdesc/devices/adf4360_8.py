"""
ADF4360-8 integer-N PLL
https://www.analog.com/en/products/adf4360-8.html
"""

from ..register import Register, Field
from .device import device


class ControlLatch(Register):
    """
    Control Latch
    """

    control_bits = Field(2, readonly=True)
    core_power_level = Field(2, reset=1, doc="core power level")
    counter_reset = Field(doc="counter reset")
    muxout_ctrl = Field(3, doc="muxout control")
    phase_detector_polarity = Field(reset=1, doc="phase detector polarity")
    cp_three_state = Field(doc="charge pump three-state")
    cp_gain = Field(doc="charge pump gain")
    mute_till_ld = Field(doc="mute till lockdetect")
    output_power_level = Field(2, doc="output power level")
    current_setting_1 = Field(3, reset=7, doc="current setting 1")
    current_setting_2 = Field(3, reset=7, doc="current setting 2")
    power_down_1 = Field(doc="power-down 1")
    power_down_2 = Field(doc="power-down 2")
    _reserved0 = Field(readonly=True)
    _reserved1 = Field(readonly=True)


class NCounterLatch(Register):
    """
    N-Counter Latch
    """

    control_bits = Field(2, reset=2, readonly=True)
    _reserved0 = Field(6, readonly=True)
    b_counter = Field(13, doc="13-bit B counter")
    cp_gain = Field(doc="charge pump gain")
    _reserved1 = Field(readonly=True)
    _reserved2 = Field(readonly=True)


class RCounterLatch(Register):
    """
    R-Counter Latch
    """

    control_bits = Field(2, reset=1, readonly=True)
    r_counter = Field(14, doc="14-bit reference counter")
    anti_backlash_width = Field(2, doc="anti-backlash pulse width")
    lock_detect_precision = Field(doc="lock detect precision")
    test_mode_bit = Field(doc="test mode bit")
    band_select_clock = Field(2, doc="band select clock")
    _reserved0 = Field(readonly=True)
    _reserved1 = Field(readonly=True)


@device
class ADF4360_8:
    def f_pfd(self, f_ref):
        return f_ref / self.r_counter_latch.r_counter

    def f_vco(self, f_ref):
        f_pfd = self.f_pfd(f_ref)
        return self.n_counter_latch.b_counter * f_pfd

    def muxout_ctrl(self):
        return [
            "3-STATE",
            "DIGITAL_LD",
            "N_DIV",
            "DVDD",
            "R_DIV",
            "RESERVED",
            "RESERVED",
            "DGND",
        ][self.control_latch.muxout_ctrl]
