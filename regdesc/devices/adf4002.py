from ..register import Register, Field
from .device import device


class InitLatch(Register):
    control_bits = Field(2, reset=3, readonly=True)
    counter_reset = Field(doc="counter reset")
    power_down_1 = Field(doc="power-down 1")
    muxout_ctrl = Field(3, doc="muxout control")
    pd_polarity = Field(reset=1, doc="PD polarity")
    cp_three_state = Field(doc="charge pump three-state")
    fastlock_enable = Field(doc="fastlock enable")
    fastlock_mode = Field(doc="fastlock mode")
    timer_counter_control = Field(4, doc="timer counter control")
    current_setting_1 = Field(3, reset=7, doc="current setting 1")
    current_setting_2 = Field(3, reset=7, doc="current setting 2")
    power_down_2 = Field(doc="power-down 2")
    _reserved0 = Field(2, readonly=True)


class FunctionLatch(InitLatch):
    control_bits = Field(2, reset=2, readonly=True)
    counter_reset = Field(doc="counter reset")
    power_down_1 = Field(doc="power-down 1")
    muxout_ctrl = Field(3, doc="muxout control")
    pd_polarity = Field(reset=1, doc="PD polarity")
    cp_three_state = Field(doc="charge pump three-state")
    fastlock_enable = Field(doc="fastlock enable")
    fastlock_mode = Field(doc="fastlock mode")
    timer_counter_control = Field(4, doc="timer counter control")
    current_setting_1 = Field(3, reset=7, doc="current setting 1")
    current_setting_2 = Field(3, reset=7, doc="current setting 2")
    power_down_2 = Field(doc="power-down 2")
    _reserved0 = Field(2, readonly=True)


class NCounterLatch(Register):
    control_bits = Field(2, reset=1, readonly=True)
    _reserved0 = Field(6, readonly=True)
    n_counter = Field(13, reset=8, doc="13-bit N counter")
    cp_gain = Field(doc="charge pump gain")
    _reserved1 = Field(2, readonly=True)


class RCounterLatch(Register):
    control_bits = Field(2, readonly=True)
    r_counter = Field(14, reset=1, doc="14-bit reference counter")
    anti_backlash_width = Field(2, doc="anti-backlash width")
    test_mode = Field(2, doc="test mode bits")
    lock_detect_precision = Field(doc="lock detect precision")
    _reserved0 = Field(3, readonly=True)


@device
class ADF4002:
    def f_pfd(self, f_ref):
        return f_ref / self.r_counter_latch.r_counter

    def f_vco(self, f_ref):
        return self.f_pfd(f_ref) * self.n_counter_latch.n_counter

    def muxout_ctrl(self):
        return [
            "3-STATE",
            "DIGITAL_LD",
            "N_DIV",
            "DVDD",
            "R_DIV",
            "ANALOG_LD",
            "SDO",
            "DGND",
        ][self.function_latch.muxout_ctrl]
