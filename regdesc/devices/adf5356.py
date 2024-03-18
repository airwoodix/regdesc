"""
ADF5356 GHz PLL
https://www.analog.com/en/products/adf5356.html
"""

from types import SimpleNamespace

from ..register import Register, Field
from .device import device


class R0(Register):
    control_bits = Field(4, readonly=True)
    int_value = Field(16, doc="16-bit integer value")
    prescaler = Field(doc="prescaler")
    autocal = Field(doc="autocal")
    _reserved0 = Field(10)


class R1(Register):
    control_bits = Field(4, reset=1, readonly=True)
    main_frac_value = Field(24, doc="24-bit main fractional value")
    _reserved0 = Field(4, readonly=True)


class R2(Register):
    control_bits = Field(4, reset=2, readonly=True)
    aux_mod_lsb_value = Field(14, doc="14-bit auxiliary modulus LSB value")
    aux_frac_lsb_value = Field(14, doc="14-bit auxiliary fractional LSB value")


class R3(Register):
    control_bits = Field(4, reset=3, readonly=True)
    phase_value = Field(24, doc="24-bit phase value")
    phase_adjust = Field(doc="phase adjust")
    phase_resync = Field(doc="phase resync")
    sd_load_reset = Field(doc="SD load reset")
    _reserved0 = Field(readonly=True)


class R4(Register):
    control_bits = Field(4, reset=4, readonly=True)
    counter_reset = Field(doc="counter reset")
    cp_three_state = Field(doc="charge pump three state")
    power_down = Field(doc="Power-down")
    pd_polarity = Field(doc="Phase detector polarity")
    mux_logic = Field(doc="MUX logic")
    ref_mode = Field(doc="REF mode")
    current_setting = Field(4, doc="current setting")
    double_buff = Field(doc="double buff")
    r_counter = Field(10, doc="10-bit R counter")
    r_divider = Field(doc="reference divider enable")
    r_doubler = Field(doc="reference doubler_enable")
    muxout = Field(3, doc="muxout control")
    _reserved0 = Field(2, readonly=True)


class R5(Register):
    control_bits = Field(4, reset=5, readonly=True)
    _reserved0 = Field(28, reset=0x800020, readonly=True)


class R6(Register):
    control_bits = Field(4, reset=6, readonly=True)
    rf_output_a_power = Field(2, doc="RF output A power")
    rf_output_a_enable = Field(doc="RF output A enable")
    _reserved0 = Field(3, readonly=True)
    rf_output_b_enable = Field(doc="RF output B enable")
    mute_till_ld = Field(doc="Mute till lock-detect")
    _reserved1 = Field(readonly=True)
    cp_bleed_current = Field(8, doc="charge pump bleed current")
    rf_divider_select = Field(3, doc="RF divider select")
    fb_select = Field(doc="feedback select")
    _reserved2 = Field(4, reset=0b1010, readonly=True)
    negative_bleed = Field(doc="negative bleed")
    gate_bleed = Field(doc="gate bleed")
    bleed_polarity = Field(doc="bleed polarity")


class R7(Register):
    control_bits = Field(4, reset=7, readonly=True)
    ld_mode = Field(doc="lockdetect mode")
    frac_n_ld_precision = Field(2, doc="frac-n lockdetect precision")
    lol_mode = Field(doc="lol mode")
    ld_cycle_count = Field(2, doc="lockdetect cycle count")
    _reserved0 = Field(15, readonly=True)
    le_sync = Field(doc="LE sync")
    _reserved1 = Field(reset=1, readonly=True)
    le_sel_sync_edge = Field(doc="LE selection sync edge")
    _reserved2 = Field(4, readonly=True)


class R8(Register):
    control_bits = Field(4, reset=8, readonly=True)
    _reserved = Field(28, reset=0x1559656, readonly=True)


class R9(Register):
    control_bits = Field(4, reset=9, readonly=True)
    synth_lock_timeout = Field(5, doc="synthesizer lock timeout")
    autocal_timeout = Field(5, doc="automatic level calibration timeout")
    timeout = Field(10, doc="timeout")
    vco_band_division = Field(8, doc="VCO band division")


class R10(Register):
    control_bits = Field(4, reset=10, readonly=True)
    adc_enable = Field(doc="ADC enable")
    adc_conv = Field(doc="ADC conversion")
    adc_clk_div = Field(8, doc="ADC clock divider")
    _reserved0 = Field(18, reset=0x300, readonly=True)


class R11(Register):
    control_bits = Field(4, reset=11, readonly=True)
    _reserved0 = Field(20, reset=0x61200, readonly=True)
    vco_band_hold = Field(doc="VCO band hold")
    _reserved1 = Field(7, readonly=True)


class R12(Register):
    control_bits = Field(4, reset=12, readonly=True)
    _reserved = Field(8, reset=0x5F, readonly=True)
    phase_resync_clk_value = Field(20, doc="phase resync clock value")


class R13(Register):
    control_bits = Field(4, reset=13, readonly=True)
    aux_mod_msb_value = Field(14, doc="14-bit auxiliary modulus MSB value")
    aux_frac_msb_value = Field(14, doc="14-bit auxiliary fractional MSB value")


@device
class ADF5356:
    def f_pfd(self, f_ref):
        p = self.r_params()
        return f_ref * ((1 + p.d) / (p.r * (1 + p.t)))

    def f_vco(self, f_ref):
        f_pfd = self.f_pfd(f_ref)
        p = self.pll_params()
        return f_pfd * (p.int + (p.frac1 + p.frac2 / p.mod2) / p.mod1)

    def f_outA(self, f_ref):
        div = 1 << self.r6.rf_divider_select
        return self.f_vco(f_ref) / div

    def f_outB(self, f_ref):
        return 2 * self.f_vco(f_ref)

    def pll_params(self):
        return SimpleNamespace(
            int=self.r0.int_value,
            frac1=self.r1.main_frac_value,
            frac2=(self.r13.aux_frac_msb_value << 14) + self.r2.aux_frac_lsb_value,
            mod1=(1 << 24),
            mod2=(self.r13.aux_mod_msb_value << 14) + self.r2.aux_mod_lsb_value,
        )

    def r_params(self):
        return SimpleNamespace(d=self.r4.r_doubler, r=self.r4.r_counter, t=self.r4.r_divider)

    def muxout_ctrl(self):
        return [
            "3-STATE",
            "DVDD",
            "SDGND",
            "R_DIV",
            "N_DIV",
            "ANALOG_LD",
            "DIGITAL_LD",
            "RESERVED",
        ][self.r4.muxout]
