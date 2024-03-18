"""
TRF372017 - Integrated IQ Modulator PLL/VCO
https://www.ti.com/product/TRF372017
"""

from ..register import Register, Field
from .device import device


class R1(Register):
    address = Field(5, reset=0x9, readonly=True)
    rdiv = Field(13, reset=1, doc="13-bit reference divider value")
    _rsv0 = Field(1, readonly=True)
    ref_inv = Field(1, doc="Invert clock polarity; 1 = use falling edge")
    neg_vco = Field(1, reset=1, doc="VCO polarity control; 1 = negative slope")
    icp = Field(5, reset=10, doc="Charge pump current")
    icpdouble = Field(1, doc="1 = set ICP to double the current")
    cal_clk_sel = Field(4, reset=8, doc="mult/div for VCO calibration clock from PFD frequency")
    _rsv1 = Field(1, readonly=True)


class R2(Register):
    address = Field(5, reset=0xA, readonly=True)
    nint = Field(16, reset=0x80, doc="PLL N-divider division setting")
    pll_div_sel = Field(2, reset=1, doc="Division ratio of divider in front of prescaler")
    prsc_sel = Field(1, reset=1, doc="Set prescaler modulus")
    _rsv = Field(2, readonly=True)
    vco_sel = Field(2, reset=2, doc="Select VCO")
    vcosel_mode = Field(1, doc="Enable single VCO auto-calibration mode")
    cal_acc = Field(2, doc="Error count during the cap array calibration")
    en_cal = Field(1, doc="Execute a VCO frequency auto-calibration. Resets automatically")


class R3(Register):
    address = Field(5, reset=0xB, readonly=True)
    nfrac = Field(25, doc="Fractional PLL N divider value")
    _rsv = Field(2, readonly=True)


class R4(Register):
    address = Field(5, reset=0xC, readonly=True)
    pwd_pll = Field(1, doc="Power-down all PLL blocks")
    pwd_cp = Field(1, doc="Power-down charge pump")
    pwd_vco = Field(1, doc="Power-down VCO")
    pwd_vcomux = Field(1, doc="Power-down all VCO mux blocks")
    pwd_div124 = Field(1, doc="Power-down RF divider in PLL feedback")
    pwd_presc = Field(1, doc="Power-down programmable prescaler")
    _rsv = Field(1, readonly=True)
    pwd_out_buff = Field(1, reset=1, doc="Power-down output buffer")
    pwd_lo_div = Field(1, reset=1, doc="Power-down frequency divider in LO output chain")
    pwd_tx_div = Field(1, reset=1, doc="Power-down frequency divider in modulator chain")
    pwd_bb_vcm = Field(1, reset=1, doc="Power-down baseband input DC common block")
    pwd_dc_off = Field(1, reset=1, doc="Power-down baseband input DC offset control block")
    en_extvco = Field(1, doc="Enable external LO/VCO input buffer")
    en_isource = Field(1, doc="Enable offset current at charge pumpt output")
    ld_ana_prec = Field(2, doc="Analog lock-detect precision")
    cp_tristate = Field(2, doc="Set charge-pump output in tristate mode")
    speedup = Field(1, doc="Speed up PLL and Tx blocks")
    ld_dig_prec = Field(1, doc="Lock detector precision")
    en_dith = Field(1, reset=1, doc="Enable delta-sigma modulator dither")
    mod_ord = Field(2, reset=2, doc="Delta-sigma modulator order")
    dith_sel = Field(1, doc="Select dither mode for delta-sigma modulator")
    del_sd_clk = Field(2, reset=2, doc="Delta-sigma modulator clock delay")
    en_frac = Field(1, doc="Enable fractional mode")


class R5(Register):
    address = Field(5, reset=0xD, readonly=True)
    vcobias_rtrim = Field(3, reset=4, doc="VCO bias resistor trimming")
    pllbias_rtrim = Field(2, reset=2, doc="PLL bias resistor trimming")
    vco_bias = Field(4, reset=8, doc="VCO bias reference current")
    vcobuf_bias = Field(2, reset=2, doc="VCO buffer bias reference current")
    vcomux_bias = Field(2, reset=2, doc="VCO muxing buffer bias reference current")
    bufout_bias = Field(2, reset=2, doc="PLL output buffer bias reference current")
    _rsv0 = Field(2, reset=2, readonly=True)
    vco_cal_ib = Field(1, doc="Bias current type for VCO calibration circuit")
    vco_rel_ref = Field(3, reset=4, doc="VCO calibration reference voltage trimming")
    vco_ampl_ctrl = Field(2, reset=2, doc="Signal amplitude at the VCO mux input")
    vco_vb_ctrl = Field(2, reset=2, doc="VCO core bias voltage control")
    _rsv1 = Field(1, readonly=True)
    en_ld_isource = Field(1, reset=1, doc="Enable monitoring of LD to turn on Isource")


class R6(Register):
    address = Field(5, reset=0xE, readonly=True)
    ioff = Field(8, reset=0x80, doc="Iref current for I DC offset")
    qoff = Field(8, reset=0x80, doc="Iref current for Q DC offset")
    vref_sel = Field(3, reset=4, doc="Vref in BB common mode generation circuit")
    tx_div_sel = Field(2, doc="Tx path divider")
    lo_div_sel = Field(2, doc="LO path divider")
    tx_div_bias = Field(2, reset=2, doc="Tx divider bias reference current")
    lo_div_bias = Field(2, reset=2, doc="LO divider bias reference current")


class R7(Register):
    address = Field(5, reset=0xF, readonly=True)
    _rsv0 = Field(2, readonly=True)
    vco_trim = Field(6, reset=0x20, doc="VCO cap array control bits")
    _rsv1 = Field(1, readonly=True)
    vco_test_mode = Field(1, doc="Measure max/min frequency of each VCO")
    cal_bypass = Field(1, doc="Bypass VCO auto-calibration")
    mux_ctrl = Field(3, reset=1, doc="Signal for test output")
    isource_sink = Field(1, doc="Charge pump offset current polarity")
    isource_trim = Field(3, reset=4, doc="Isource bias current in frac-n mode")
    pd_tc = Field(2, doc="Time constant control for PWD_OUT_BUFF")
    ib_vcm_sel = Field(1, doc="Current type for common mode bias generation block")
    _rsv2 = Field(3, reset=4, readonly=True)
    dcoffset_i = Field(2, reset=2, doc="Adjust BB input DC offset reference current")
    vco_bias_sel = Field(1, doc="VCO_BIAS trim settings stored in EEPROM")


@device
class TRF372017:
    frac_modulus = 1 << 25

    def f_pfd(self, f_ref):
        return f_ref / self.r1.rdiv

    def f_vco(self, f_ref):
        f_pfd = self.f_pfd(f_ref)

        n = self.r2.nint
        if self.r4.en_frac:
            n += self.r3.nfrac / self.frac_modulus

        assert self.r2.pll_div_sel != 3, "Invalid pll_div_sel"

        return f_pfd * (1 << self.r2.pll_div_sel) * n

    def f_lo(self, f_ref):
        return self.f_vco(f_ref) / (1 << self.r6.lo_div_sel)

    def f_tx(self, f_ref):
        return self.f_vco(f_ref) / (1 << self.r6.tx_div_sel)
