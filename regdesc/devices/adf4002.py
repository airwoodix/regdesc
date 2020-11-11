from ..register import Register, Field


class InitLatch(Register):
    control_bits = Field("control bits", width=2, value=3)
    counter_reset = Field("counter reset", width=1, value=0)
    power_down_1 = Field("power-down 1", width=1, value=0)
    muxout_ctrl = Field("muxout control", width=3, value=1)
    pd_polarity = Field("PD polarity", width=1, value=1)
    cp_three_state = Field("CP three-state", width=1, value=0)
    fastlock_enable = Field("fastlock enable", width=1, value=0)
    fastlock_mode = Field("fastlock mode", width=1, value=0)
    timer_counter_control = Field("timer counter control", width=4, value=0)
    current_setting_1 = Field("current setting 1", width=3, value=7)
    current_setting_2 = Field("current setting 2", width=3, value=7)
    power_down_2 = Field("power-down 2", width=1, value=0)
    _reserved0 = Field("reserved", width=2, value=0)


class FunctionLatch(Register):
    control_bits = Field("control bits", width=2, value=2)
    counter_reset = Field("counter reset", width=1, value=0)
    power_down_1 = Field("power-down 1", width=1, value=0)
    muxout_ctrl = Field("muxout control", width=3, value=1)
    pd_polarity = Field("PD polarity", width=1, value=1)
    cp_three_state = Field("CP three-state", width=1, value=0)
    fastlock_enable = Field("fastlock enable", width=1, value=0)
    fastlock_mode = Field("fastlock mode", width=1, value=0)
    timer_counter_control = Field("timer counter control", width=4, value=0)
    current_setting_1 = Field("current setting 1", width=3, value=7)
    current_setting_2 = Field("current setting 2", width=3, value=7)
    power_down_2 = Field("power-down 2", width=1, value=0)
    _reserved0 = Field("reserved", width=2, value=0)


class NCounterLatch(Register):
    control_bits = Field("control bits", width=2, value=1)
    _reserved0 = Field("reserved", width=6, value=0)
    n_counter = Field("13-bit N counter", width=13, value=8)
    cp_gain = Field("CP gain", width=1, value=0)
    _reserved1 = Field("reserved_", width=2, value=0)


class RCounterLatch(Register):
    control_bits = Field("control bits", width=2, value=0)
    r_counter = Field("14-bit reference counter", width=14, value=1)
    anti_backlash_width = Field("anti-backlash width", width=2, value=0)
    test_mode = Field("test mode bits", width=2, value=0)
    lock_detect_precision = Field("lock detect precision", width=1, value=0)
    _reserved0 = Field("reserved", width=3, value=0)


class Device:
    init_latch = InitLatch()
    function_latch = FunctionLatch()
    r_counter_latch = RCounterLatch()
    n_counter_latch = NCounterLatch()

    @classmethod
    def f_pfd(cls, f_ref):
        return f_ref / cls.r_counter_latch.r_counter

    @classmethod
    def f_vco(cls, f_ref):
        return cls.f_pfd(f_ref) * cls.n_counter_latch.n_counter

    @classmethod
    def muxout_ctrl(cls):
        return [
            "3-STATE",
            "DIGITAL_LD",
            "N_DIV",
            "DVDD",
            "R_DIV",
            "ANALOG_LD",
            "SDO",
            "DGND",
        ][cls.function_latch.muxout_ctrl]
