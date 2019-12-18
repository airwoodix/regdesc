from ..register import Register, Field


class ControlLatch(Register):
    control_bits = Field("control bits", width=2, value=0)
    core_power_level = Field("core power level", width=2, value=1)
    counter_reset = Field("counter reset", width=1, value=0)
    muxout_ctrl = Field("muxout control", width=3, value=0)
    phase_detector_polarity = Field("phase detector polarity",
                                    width=1, value=1)
    cp_three_state = Field("cp three-state", width=1, value=0)
    cp_gain = Field("cp gain", width=1, value=0)
    mute_till_ld = Field("mute till lockdetect", width=1, value=1)
    output_power_level = Field("output power level", width=2, value=0)
    current_setting_1 = Field("current setting 1", width=3, value=7)
    current_setting_2 = Field("current setting 2", width=3, value=7)
    power_down_1 = Field("power-down 1", width=1, value=0)
    power_down_2 = Field("power-down 2", width=1, value=0)
    _reserved0 = Field("reserved", width=1, value=0)
    _reserved1 = Field("reserved", width=1, value=0)


class NCounterLatch(Register):
    control_bits = Field("control bits", width=2, value=2)
    _reserved0 = Field("reserved", width=6, value=0)
    b_counter = Field("13-bit B counter", width=13, value=0)
    cp_gain = Field("cp gain", width=1, value=0)
    _reserved1 = Field("reserved", width=1, value=0)
    _reserved2 = Field("reserved", width=1, value=0)


class RCounterLatch(Register):
    control_bits = Field("control bits", width=2, value=1)
    r_counter = Field("14-bit reference counter", width=14, value=0)
    anti_backlash_width = Field("anti-backlash pulse width",
                                width=2, value=0)
    lock_detect_precision = Field("lock detect precision",
                                  width=1, value=0)
    test_mode_bit = Field("test mode bit", width=1, value=0)
    band_select_clock = Field("band select clock", width=2, value=0)
    _reserved0 = Field("reserved", width=1, value=0)
    _reserved1 = Field("reserved", width=1, value=0)


class Device:
    r_counter_latch = RCounterLatch()
    control_latch = ControlLatch()
    n_counter_latch = NCounterLatch()

    @classmethod
    def f_pfd(cls, f_ref):
        return f_ref / cls.r_counter_latch.r_counter

    @classmethod
    def f_vco(cls, f_ref):
        f_pfd = cls.f_pfd(f_ref)
        return cls.n_counter_latch.b_counter * f_pfd

    @classmethod
    def muxout_ctrl(cls):
        return ["3-STATE",
                "DIGITAL_LD",
                "N_DIV",
                "DVDD",
                "R_DIV",
                "RESERVED",
                "RESERVED",
                "DGND"][cls.control_latch.muxout_ctrl]
