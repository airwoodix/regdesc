"""
AD9910 GSps Direct Digital Synthesizer
https://www.analog.com/en/products/ad9910.html
"""

from ..register import Field, Register
from .device import device


class CFR1(Register):
    """
    Control Function Register 1
    """

    __address__ = 0x00

    lsb_first = Field(doc="LSB first")
    sdio_input_only = Field(doc="SDIO input only")
    _reserved0 = Field(readonly=True)
    external_power_down_ctrl = Field(doc="External power-down control")
    aux_dac_power_down = Field(doc="Aux DAC power-down")
    refclk_input_power_down = Field(doc="REFCLK input power-down")
    dac_power_down = Field(doc="DAC power-down")
    digital_power_down = Field(doc="Digital power-down")

    select_auto_osk = Field(doc="Select auto OSK")
    osk_enable = Field(doc="OSK enable")
    load_arr_at_io_update = Field(doc="Load ARR @ I/O update")
    clear_phase_accumulator = Field(doc="Clear phase accumulator")
    clear_digital_ramp_accumulator = Field(doc="Clear digital ramp accumulator")
    autoclear_phase_accumulator = Field(doc="Autoclear phase accumulator")
    autoclear_digital_ramp_accumulator = Field(doc="Autoclear digital ramp accumulator")
    load_lrr_at_io_update = Field(doc="Load LRR @ I/O update")

    select_dds_sine_output = Field(doc="Select DDS sine output")
    internal_profile_control = Field(4, doc="Internal profile control")
    _reserved1 = Field(readonly=True)
    inverse_sinc_filter_enable = Field(doc="Inverse sinc filter enable")
    manual_osk_external_control = Field(doc="Manuel OSK external control")

    _reserved2 = Field(5, readonly=True)
    ram_playback_destination = Field(2, doc="RAM playback destination")
    ram_enable = Field(doc="RAM enable")


class CFR2(Register):
    """
    Control Function Register 2
    """

    __address__ = 0x01

    fm_gain = Field(4, doc="FM gain")
    parallel_data_port_enable = Field(doc="Parallel data port enable")
    sync_timing_validation_disable = Field(
        reset=1, doc="Sync timing validation disable"
    )
    data_assembler_hold_last_value = Field(doc="Data assembler hold last value")
    matched_latency_enable = Field(doc="Matched latency enable")

    _reserved0 = Field(readonly=True)
    tx_enable_invert = Field(doc="TxEnable invert")
    pdclk_invert = Field(doc="PDCLK invert")
    pdclk_enable = Field(reset=1, doc="PDCLK enable")
    _reserved1 = Field(2, readonly=True)
    io_update_rate_control = Field(2, doc="I/O update rate control")

    read_effective_ftw = Field(doc="Read effective FTW")
    digital_ramp_no_dwell_low = Field(doc="Digital ramp no-dwell low")
    digital_ramp_no_dwell_high = Field(doc="Digital ramp no-dwell high")
    digital_ramp_enable = Field(doc="Digital ramp enable")
    digital_ramp_destination = Field(2, doc="Digital ramp destination")
    sync_clk_enable = Field(reset=1, doc="SYNC_CLK enable")
    internal_io_update_active = Field(doc="Internal I/O update active")

    enable_amplitude_scale_from_single_tone_profiles = Field(
        doc="Enable amplitude scale from single tone profiles"
    )
    _reserved2 = Field(7, readonly=True)


class CFR3(Register):
    """
    Control Function Register 3
    """

    __address__ = 0x02

    _reserved0 = Field(readonly=True)
    n = Field(7, doc="Divide modulus of the REFCLK PLL feedback divider")

    pll_enable = Field(doc="PLL enable")
    _reserved1 = Field(readonly=True)
    pfd_reset = Field(doc="PFD reset")
    _reserved2 = Field(3, readonly=True)
    refclk_input_divider_resetb = Field(reset=1, doc="REFCLK input divider ResetB")
    refclk_input_divider_bypass = Field(doc="REFCLK input divider bypass")

    _reserved3 = Field(3, reset=0x7, readonly=True)
    i_cp = Field(3, reset=0x7, doc="Charge pump current in the REFCLK PLL")
    _reserved4 = Field(2, readonly=True)

    vco_sel = Field(3, reset=0x7, doc="Frequency band selection for the REFCLK PLL VCO")
    _reserved5 = Field(reset=1, readonly=True)
    drv0 = Field(2, reset=1, doc="REFCLK_OUT pin control")
    _reserved6 = Field(2, readonly=True)


class AuxDACControl(Register):
    """
    Auxiliary DAC Control Register
    """

    __address__ = 0x03

    fsc = Field(8, reset=0x7F, doc="Full scale output current of the main DAC")
    _reserved0 = Field(24, readonly=True)


class IOUpdateRate(Register):
    """
    I/O Update Rate Register
    """

    __address__ = 0x04

    io_update_rate = Field(32, reset=0xFFFFFFFF, doc="I/O update rate")


class FTW(Register):
    """
    Frequency Tuning Word Register
    """

    __address__ = 0x07

    ftw = Field(32, doc="Frequency tuning word")


class POW(Register):
    """
    Phase Offset Word Register
    """

    __address__ = 0x08

    pow = Field(16, doc="Phase offset word")


class ASF(Register):
    """
    Amplitude Scale Factor Register
    """

    __address__ = 0x09

    amplitude_step_size = Field(2, doc="Amplitude step size")
    asf = Field(14, doc="Amplitude scale factor")
    amplitude_ramp_rate = Field(16, doc="Amplitude ramp rate")


class MultichipSync(Register):
    """
    Multichip Sync Register
    """

    __address__ = 0x0A

    _reserved0 = Field(3, readonly=True)
    input_sync_receiver_delay = Field(5, doc="Input sync receiver delay")

    _reserved1 = Field(3, readonly=True)
    output_sync_generator_delay = Field(5, doc="Output sync generator delay")

    _reserved2 = Field(2, readonly=True)
    sync_state_preset_value = Field(6, doc="Sync state preset value")

    _reserved3 = Field(readonly=True)
    sync_generator_polarity = Field(doc="Sync generator polarity")
    sync_generator_enable = Field(doc="Sync generator enable")
    sync_receiver_enable = Field(doc="Sync receiver enable")
    sync_validation_delay = Field(4, doc="Sync validation delay")


class DigitalRampLimit(Register):
    """
    Digital Ramp Limit Register
    """

    __address__ = 0x0B

    lower_limit = Field(32, doc="Digital ramp lower limit")
    upper_limit = Field(32, doc="Digital ramp upper limit")


class DigitalRampStepSize(Register):
    """
    Digital Ramp Step Size Register
    """

    __address__ = 0x0C

    increment_step_size = Field(32, doc="Digital ramp increment step size")
    decrement_step_size = Field(32, doc="Digital ramp decrement step size")


class DigitalRampRate(Register):
    """
    Digital Ramp Rate Register
    """

    __address__ = 0x0D

    positive_slope_rate = Field(16, doc="Digital ramp positive slope rate")
    negative_slope_rate = Field(16, doc="Digital ramp negative slope rate")


_tpl = """
class SingleToneProfile{num}(Register):
    '''
    Single Tone Profile {num} Register
    '''
    __address__ = {addr}

    ftw = Field(32, doc="Frequency tuning word {num}")
    pow = Field(16, doc="Phase offset word {num}")
    asf = Field(14, reset={asf_reset}, doc="Amplitude scale factor {num}")
    _reserved0 = Field(2, readonly=True)


class RAMProfile{num}(Register):
    '''
    RAM Profile {num} Register
    '''
    __address__ = {addr}

    mode_control = Field(3, doc="RAM profile {num} mode control")
    zero_crossing = Field(doc="Zero-crossing function enable")
    _reserved0 = Field(readonly=True)
    no_dwell_high = Field(doc="No-dwell high")
    _reserved1 = Field(2, readonly=True)

    _reserved2 = Field(6, readonly=True)
    waveform_start_address = Field(10, doc="RAM profile {num} waveform start address")
    _reserved3 = Field(6, readonly=True)
    waveform_stop_address = Field(10, doc="RAM profile {num} waveform end address")
    address_step_rate = Field(16, doc="RAM profile {num} address step rate")
    _reserved4 = Field(8, readonly=True)
"""

for num in range(8):
    exec(_tpl.format(num=num, addr=0xE + num, asf_reset=0x8B5 if num == 0 else 0))


class RAM(Register):
    """
    RAM Register
    """

    __address__ = 0x16

    word = Field(32, doc="RAM word")


@device
class AD9910:
    pass
