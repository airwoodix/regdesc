from ..register import Register, Field
from types import SimpleNamespace


class R0(Register):
    control_bits = Field("control bits", width=4, value=0)
    int_value = Field("16-bit integer value", width=16)
    prescaler = Field("prescaler", width=1)
    autocal = Field("autocal", width=1)
    _reserved = Field("reserved", width=10)


class R1(Register):
    control_bits = Field("control bits", width=4, value=1)
    main_frac_value = Field("24-bit main fractional value", width=24)
    _reserved = Field("reserved", width=4)


class R2(Register):
    control_bits = Field("control bits", width=4, value=2)
    aux_mod_lsb_value = Field("14-bit auxiliary modulus LSB value", width=14)
    aux_frac_lsb_value = Field("14-bit auxiliary fractional LSB value", width=14)


class R3(Register):
    control_bits = Field("control bits", width=4, value=3)
    phase_value = Field("24-bit phase value", width=24)
    phase_adjust = Field("phase adjust", width=1)
    phase_resync = Field("phase resync", width=1)
    sd_load_reset = Field("SD load reset", width=1)
    _reserved = Field("reserved", width=1)


class R4(Register):
    control_bits = Field("control bits", width=4, value=4)
    counter_reset = Field("counter reset", width=1)
    cp_three_state = Field("CP three state", width=1)
    power_down = Field("Power-down", width=1)
    pd_polarity = Field("PD polarity", width=1)
    mux_logic = Field("MUX logic", width=1)
    ref_mode = Field("REF mode", width=1)
    current_setting = Field("current setting", width=4)
    double_buff = Field("double buff", width=1)
    r_counter = Field("10-bit R counter", width=10)
    r_divider = Field("reference divider", width=1)
    r_doubler = Field("reference doubler", width=1)
    muxout = Field("muxout", width=3)
    _reserved = Field("reserved", width=2)


class R5(Register):
    control_bits = Field("control bits", width=4, value=5)
    _reserved = Field("reserved", width=28)


class R6(Register):
    control_bits = Field("control bits", width=4, value=6)
    rf_output_a_power = Field("RF output A power", width=2)
    rf_output_a_enable = Field("RF output A enable", width=1)
    _reserved0 = Field("reserved", width=3)
    rf_output_b_enable = Field("RF output B enable", width=1)
    mute_till_ld = Field("MTLD", width=1)
    _reserved1 = Field("reserved", width=1)
    cp_bleed_current = Field("charge pump bleed current", width=8)
    rf_divider_select = Field("RF divider select", width=3)
    fb_select = Field("feedback select", width=1)
    _reserved2 = Field("reserved", width=4, value=0b1010)
    negative_bleed = Field("negative bleed", width=1)
    gate_bleed = Field("gate bleed", width=1)
    bleed_polarity = Field("bleed polarity", width=1)


class R7(Register):
    control_bits = Field("control bits", width=4, value=7)
    ld_mode = Field("lockdetect mode", width=1)
    frac_n_ld_precision = Field("frac-n lockdetect precision", width=2)
    lol_mode = Field("lol mode", width=1)
    ld_cycle_count = Field("lockdetect cycle count", width=2)
    _reserved0 = Field("reserved", width=15)
    le_sync = Field("LE sync", width=1)
    _reserved1 = Field("reserved", width=1, value=1)
    le_sel_sync_edge = Field("LE selection sync edge", width=1)
    _reserved2 = Field("reserved", width=4)


class R8(Register):
    control_bits = Field("control bits", width=4, value=8)
    _reserved = Field("reserved", width=28, value=0x1559656)


class R9(Register):
    control_bits = Field("control bits", width=4, value=9)
    synth_lock_timeout = Field("synthesizer lock timeout", width=5)
    autocal_timeout = Field("automatic level calibration timeout", width=5)
    timeout = Field("timeout", width=10)
    vco_band_division = Field("VCO band division", width=8)


class R10(Register):
    control_bits = Field("control_bits", width=4, value=10)
    adc_enable = Field("ADC enable", width=1)
    adc_conv = Field("ADC conversion", width=1)
    adc_clk_div = Field("ADC clock divider", width=8)
    _reserved = Field("reserved", width=18, value=0x300)


class R11(Register):
    control_bits = Field("control bits", width=4, value=11)
    _reserved0 = Field("reserved", width=20, value=0x61200)
    vco_band_hold = Field("VCO band hold", width=1)
    _reserved1 = Field("reserved", width=7)


class R12(Register):
    control_bits = Field("control bits", width=4, value=12)
    _reserved = Field("reserved", width=8, value=0x5F)
    phase_resync_clk_value = Field("phase resync clock value", width=20)


class R13(Register):
    control_bits = Field("control bits", width=4, value=13)
    aux_mod_msb_value = Field("14-bit auxiliary modulus MSB value", width=14)
    aux_frac_msb_value = Field("14-bit auxiliary fractional MSB value", width=14)


class Device:
    r0 = R0()
    r1 = R1()
    r2 = R2()
    r3 = R3()
    r4 = R4()
    r5 = R5()
    r6 = R6()
    r7 = R7()
    r8 = R8()
    r9 = R9()
    r10 = R10()
    r11 = R11()
    r12 = R12()
    r13 = R13()

    @classmethod
    def f_pfd(cls, f_ref):
        p = cls.r_params()
        return f_ref * ((1 + p.d) / (p.r * (1 + p.t)))

    @classmethod
    def f_vco(cls, f_ref):
        f_pfd = cls.f_pfd(f_ref)
        p = cls.pll_params()
        return f_pfd * (p.int + (p.frac1 + p.frac2 / p.mod2) / p.mod1)

    @classmethod
    def f_outA(cls, f_ref):
        div = 1 << cls.r6.rf_divider_select
        return cls.f_vco(f_ref) / div

    @classmethod
    def f_outB(cls, f_ref):
        return 2 * cls.f_vco(f_ref)

    @classmethod
    def pll_params(cls):
        return SimpleNamespace(
            int=cls.r0.int_value,
            frac1=cls.r1.main_frac_value,
            frac2=(cls.r13.aux_frac_msb_value << 14) + cls.r2.aux_frac_lsb_value,
            mod1=(1 << 24),
            mod2=(cls.r13.aux_mod_msb_value << 14) + cls.r2.aux_mod_lsb_value,
        )

    @classmethod
    def r_params(cls):
        return SimpleNamespace(
            d=cls.r4.r_doubler, r=cls.r4.r_counter, t=cls.r4.r_divider
        )

    @classmethod
    def muxout_ctrl(cls):
        return [
            "3-STATE",
            "DVDD",
            "SDGND",
            "R_DIV",
            "N_DIV",
            "ANALOG_LD",
            "DIGITAL_LD",
            "RESERVED",
        ][cls.r4.muxout]
