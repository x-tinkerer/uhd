#
# Copyright 2023 Ettus Research, a National Instruments Brand
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""Streaming tests for UHD devices using pytest.
"""

from pathlib import Path

import batch_run_benchmark_rate
import pytest
import test_length_utils
from test_length_utils import Test_Length_Full, Test_Length_Smoke, Test_Length_Stress

ARGNAMES_DUAL_SFP = [
    "dual_sfp",
    "rate",
    "rx_rate",
    "rx_channels",
    "tx_rate",
    "tx_channels",
    "tx_sample_align",
]


def parametrize_test_length(metafunc, test_length, fast_params, stress_params):
    """Parametrize the test length for the test cases based on test_length smoke…full."""
    argnames = ["iterations", "duration"]

    # select how long to run tests
    if test_length == Test_Length_Smoke or test_length == Test_Length_Full:
        argvalues = [
            pytest.param(fast_params.iterations, fast_params.duration, id="fast"),
        ]
    elif test_length == Test_Length_Stress:
        argvalues = [
            pytest.param(stress_params.iterations, stress_params.duration, id="stress"),
        ]

    metafunc.parametrize(argnames, argvalues)


def _generate_n310_test_cases(metafunc, test_length):
    test_cases = [
        # fmt: off
        # Test Lengths                                         dual_sfp  rate     rx_rate  rx_channels tx_rate  tx_channels tx_sample_align test case ID                # noqa: W505
        # ---------------------------------------------------------------------------------------------------------------------------------------------- # noqa: W505
        [{},                                      pytest.param(False,    153.6e6, 153.6e6, "0",        0,       "",         None,           id="1x10GbE-1xRX@153.6e6")],
        [{},                                      pytest.param(False,    153.6e6, 153.6e6, "0,1",      0,       "",         None,           id="1x10GbE-2xRX@153.6e6")],
        [{},                                      pytest.param(False,    153.6e6, 0,       "",         153.6e6, "0",        None,           id="1x10GbE-1xTX@153.6e6")],
        [{},                                      pytest.param(False,    153.6e6, 0,       "",         153.6e6, "0,1",      None,           id="1x10GbE-2xTX@153.6e6")],
        [{},                                      pytest.param(False,    153.6e6, 153.6e6, "0",        153.6e6, "0",        None,           id="1x10GbE-1xTRX@153.6e6")],
        [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(False,    153.6e6, 153.6e6, "0,1",      153.6e6, "0,1",      None,           id="1x10GbE-2xTRX@153.6e6")],
        [{},                                      pytest.param(False,    125e6,   125e6,   "0,1",      125e6,   "0,1",      None,           id="1x10GbE-2xTRX@125e6")],
        [{},                                      pytest.param(False,    62.5e6,  62.5e6,  "0,1,2,3",  0,       "",         None,           id="1x10GbE-4xRX@62.5e6")],
        [{},                                      pytest.param(False,    62.5e6,  0,       "",         62.5e6,  "0,1,2,3",  None,           id="1x10GbE-4xTX@62.5e6")],
        [{Test_Length_Smoke, Test_Length_Stress}, pytest.param(False,    62.5e6,  62.5e6,  "0,1,2,3",  62.5e6,  "0,1,2,3",  None,           id="1x10GbE-4xTRX@62.5e6")],
        [{},                                      pytest.param(True,     153.6e6, 153.6e6, "0,1",      0,       "",         None,           id="2x10GbE-2xRX@153.6e6")],
        [{},                                      pytest.param(True,     153.6e6, 0,       "",         153.6e6, "0,1",      None,           id="2x10GbE-2xTX@153.6e6")],
        [{},                                      pytest.param(True,     153.6e6, 153.6e6, "0,1",      153.6e6, "0,1",      None,           id="2x10GbE-2xTRX@153.6e6")],
        [{},                                      pytest.param(True,     153.6e6, 153.6e6, "0,1,2,3",  0,       "",         None,           id="2x10GbE-4xRX@153.6e6")],
        [{},                                      pytest.param(True,     153.6e6, 0,       "",         153.6e6, "0,1,2,3",  None,           id="2x10GbE-4xTX@153.6e6")],
        [{},                                      pytest.param(True,     153.6e6, 153.6e6, "0,1,2,3",  153.6e6, "0,1,2,3",  None,           id="2x10GbE-4xTRX@153.6e6")],
        [{},                                      pytest.param(True,     125e6,   125e6,   "0,1,2,3",  0,       "",         None,           id="2x10GbE-4xRX@125e6")],
        [{},                                      pytest.param(True,     125e6,   0,       "",         125e6,   "0,1,2,3",  None,           id="2x10GbE-4xTX@62.5e6")],
        [{Test_Length_Smoke, Test_Length_Stress}, pytest.param(True,     125e6,   125e6,   "0,1,2,3",  125e6,   "0,1,2,3",  None,           id="2x10GbE-4xTRX@62.5e6")],
        # fmt: on
    ]

    argvalues = test_length_utils.select_test_cases_by_length(test_length, test_cases)
    metafunc.parametrize(ARGNAMES_DUAL_SFP, argvalues)

    fast_params = test_length_utils.test_length_params(iterations=10, duration=30)
    stress_params = test_length_utils.test_length_params(iterations=2, duration=600)
    parametrize_test_length(metafunc, test_length, fast_params, stress_params)


def _generate_n320_test_cases(metafunc, test_length):
    test_cases = [
        # fmt: off
        # Test Lengths                                         dual_sfp  rate     rx_rate  rx_channels tx_rate  tx_channels tx_algin test case ID               # noqa: W505
        # --------------------------------------------------------------------------------------------------------------------------------------------- # noqa: W505
        [{},                                      pytest.param(False,    250e6,   250e6,   "0",        0,       "",         None,           id="1x10GbE-1xRX@250e6")],
        [{},                                      pytest.param(False,    250e6,   0,       "",         250e6,   "0",        None,           id="1x10GbE-1xTX@250e6")],
        [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(False,    250e6,   250e6,   "0",        250e6,   "0",        None,           id="1x10GbE-1xTRX@250e6")],
        [{},                                      pytest.param(True,     250e6,   250e6,   "0,1",      0,       "",         None,           id="2x10GbE-2xRX@250e6")],
        [{},                                      pytest.param(True,     250e6,   0,       "",         250e6,   "0,1",      None,           id="2x10GbE-2xTX@250e6")],
        [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(True,     250e6,   250e6,   "0,1",      250e6,   "0,1",      None,           id="2x10GbE-2xTRX@250e6")],
        # fmt: on
    ]

    argvalues = test_length_utils.select_test_cases_by_length(test_length, test_cases)
    metafunc.parametrize(ARGNAMES_DUAL_SFP, argvalues)

    fast_params = test_length_utils.test_length_params(iterations=10, duration=30)
    stress_params = test_length_utils.test_length_params(iterations=2, duration=600)
    parametrize_test_length(metafunc, test_length, fast_params, stress_params)


def _generate_b210_test_cases(metafunc, test_length):
    test_cases = [
        # fmt: off
        # Test Lengths                                         dual_sfp  rate     rx_rate  rx_channels tx_rate  tx_channels tx_sample_align test case ID          # noqa: W505
        # ---------------------------------------------------------------------------------------------------------------------------------------- # noqa: W505
        [{},                                      pytest.param(False,    61.44e6, 61.44e6, "0",        0,       "",         None,           id="1xRX@61.44e6")],
        [{},                                      pytest.param(False,    30.72e6, 30.72e6, "0,1",      0,       "",         None,           id="2xRX@30.72e6")],
        [{},                                      pytest.param(False,    61.44e6, 0,       "",         61.44e6, "0",        None,           id="1xTX@61.44e6")],
        [{},                                      pytest.param(False,    30.72e6, 0,       "",         30.72e6, "0,1",      None,           id="2xTX@30.72e6")],
        [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(False,    30.72e6, 30.72e6, "0",        30.72e6, "0",        None,           id="1xTRX@30.72e6")],
        [{},                                      pytest.param(False,    15.36e6, 15.36e6, "0,1",      15.36e6, "0,1",      None,           id="2xTRX@15.36e6")],
        # fmt: on
    ]

    argvalues = test_length_utils.select_test_cases_by_length(test_length, test_cases)
    metafunc.parametrize(ARGNAMES_DUAL_SFP, argvalues)

    fast_params = test_length_utils.test_length_params(iterations=10, duration=30)
    stress_params = test_length_utils.test_length_params(iterations=2, duration=600)
    parametrize_test_length(metafunc, test_length, fast_params, stress_params)


def _generate_e320_test_cases(metafunc, test_length):
    test_cases = [
        # fmt: off
        # Test Lengths                                         dual_sfp  rate     rx_rate  rx_channels tx_rate  tx_channels tx_sample_align test case ID          # noqa: W505
        # -------------------------------------------------------------- ------------------------------------------------------------------------- # noqa: W505
        [{},                                      pytest.param(False,    61.44e6, 61.44e6, "0",        0,       "",         None,           id="1xRX@61.44e6")],
        [{},                                      pytest.param(False,    61.44e6, 61.44e6, "0,1",      0,       "",         None,           id="2xRX@61.44e6")],
        [{},                                      pytest.param(False,    61.44e6, 0,       "",         61.44e6, "0",        None,           id="1xTX@61.44e6")],
        [{},                                      pytest.param(False,    61.44e6, 0,       "",         61.44e6, "0,1",      None,           id="2xTX@61.44e6")],
        [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(False,    61.44e6, 61.44e6, "0",        61.44e6, "0",        None,           id="1xTRX@61.44e6")],
        [{},                                      pytest.param(False,    61.44e6, 61.44e6, "0,1",      61.44e6, "0,1",      None,           id="2xTRX@61.44e6")],
        # fmt: on
    ]

    argvalues = test_length_utils.select_test_cases_by_length(test_length, test_cases)
    metafunc.parametrize(ARGNAMES_DUAL_SFP, argvalues)

    fast_params = test_length_utils.test_length_params(iterations=10, duration=30)
    stress_params = test_length_utils.test_length_params(iterations=2, duration=600)
    parametrize_test_length(metafunc, test_length, fast_params, stress_params)


def _generate_x310_test_cases(metafunc, test_length):
    test_cases = [
        # fmt: off
        # Test Lengths                                         dual_sfp  rate     rx_rate  rx_channels tx_rate  tx_channels tx_sample_align test case ID               # noqa: W505
        # --------------------------------------------------------------------------------------------------------------------------------------------- # noqa: W505
        [{},                                      pytest.param(False,    200e6,   200e6,   "0",        0,       "",         None,           id="1x10GbE-1xRX@200e6")],
        [{},                                      pytest.param(False,    100e6,   100e6,   "0,1",      0,       "",         None,           id="1x10GbE-2xRX@100e6")],
        [{},                                      pytest.param(False,    200e6,   0,       "",         200e6,   "0",        None,           id="1x10GbE-1xTX@200e6")],
        [{},                                      pytest.param(False,    100e6,   0,       "",         100e6,   "0,1",      None,           id="1x10GbE-2xTX@100e6")],
        [{},                                      pytest.param(False,    200e6,   200e6,   "0",        200e6,   "0",        None,           id="1x10GbE-1xTRX@200e6")],
        [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(False,    100e6,   100e6,   "0,1",      100e6,   "0,1",      None,           id="1x10GbE-2xTRX@100e6")],
        [{},                                      pytest.param(True,     200e6,   200e6,   "0,1",      0,       "",         None,           id="2x10GbE-2xRX@200e6")],
        [{},                                      pytest.param(True,     200e6,   0,       "",         200e6,   "0,1",      None,           id="2x10GbE-2xTX@200e6")],
        [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(True,     200e6,   200e6,   "0,1",      200e6,   "0,1",      None,           id="2x10GbE-2xTRX@200e6")],
        # fmt: on
    ]

    argvalues = test_length_utils.select_test_cases_by_length(test_length, test_cases)
    metafunc.parametrize(ARGNAMES_DUAL_SFP, argvalues)

    fast_params = test_length_utils.test_length_params(iterations=10, duration=60)
    stress_params = test_length_utils.test_length_params(iterations=2, duration=600)
    parametrize_test_length(metafunc, test_length, fast_params, stress_params)


def _generate_x310_twinrx_test_cases(metafunc, test_length):
    test_cases = [
        # fmt: off
        # Test Lengths                                         dual_sfp  rate     rx_rate  rx_channels tx_rate  tx_channels tx_sample_align test case ID              # noqa: W505
        # -------------------------------------------------------------------------------------------------------------------------------------------- # noqa: W505
        [{},                                      pytest.param(False,    100e6,   100e6,   "0,1,2",    0,       "",         None,           id="1x10GbE-3xRX@100e6")],
        [{},                                      pytest.param(False,    50e6,    50e6,    "0,1,2,3",  0,       "",         None,           id="1x10GbE-4xRX@50e6")],
        [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(True,     100e6,   100e6,   "0,1,2,3",  0,       "",         None,           id="2x10GbE-4xRX@100e6")],
        # fmt: on
    ]

    argvalues = test_length_utils.select_test_cases_by_length(test_length, test_cases)
    metafunc.parametrize(ARGNAMES_DUAL_SFP, argvalues)

    fast_params = test_length_utils.test_length_params(iterations=10, duration=30)
    stress_params = test_length_utils.test_length_params(iterations=2, duration=600)
    parametrize_test_length(metafunc, test_length, fast_params, stress_params)


def _generate_x410_test_cases(metafunc, test_length, dut_fpga):
    if dut_fpga.upper() == "CG_400":
        test_cases = [
            # fmt: off
            # Test Lengths                                         dual_sfp  rate     rx_rate  rx_channels tx_rate  tx_channels  tx_sample_align test case ID                 # noqa: W505
            # ------------------------------------------------------------------------------------------------------------------------------                  # noqa: W505 
            #[{},                                      pytest.param(False,    200e6,   200e6,   "0",        0,       "",         None,           id="1x10GbE-1xRX@200e6")],  # noqa: W505
            #[{},                                      pytest.param(False,    200e6,   100e6,   "0,1",      0,       "",         None,           id="1x10GbE-2xRX@100e6")],  # noqa: W505
            #[{},                                      pytest.param(False,    200e6,   0,       "",         200e6,   "0",        None,           id="1x10GbE-1xTX@200e6")],  # noqa: W505
            #[{},                                      pytest.param(False,    200e6,   0,       "",         100e6,   "0,1",      None,           id="1x10GbE-2xTX@100e6")],  # noqa: W505
            #[{Test_Length_Stress, Test_Length_Smoke}, pytest.param(False,    200e6,   200e6,   "0",        200e6,   "0",        None,           id="1x10GbE-1xTRX@200e6")], # noqa: W505
            #[{},                                      pytest.param(False,    200e6,   100e6,   "0,1",      100e6,   "0,1",      None,           id="1x10GbE-2xTRX@100e6")], # noqa: W505
            #[{},                                      pytest.param(True,     200e6,   200e6,   "0,1",      0,       "",         None,           id="2x10GbE-2xRX@200e6")],  # noqa: W505
            #[{},                                      pytest.param(True,     200e6,   0,       "",         200e6,   "0,1",      None,           id="2x10GbE-2xTX@200e6")],  # noqa: W505
            #[{Test_Length_Stress, Test_Length_Smoke}, pytest.param(True,     200e6,   100e6,   "0,1",      100e6,   "0,1",      None,           id="2x10GbE-2xTRX@100e6")], # noqa: W505
            [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(False,     491.52e6, 491.52e6, "0,1",    491.52e6, "0,1",      64,             id="1x100GbE-2xTRX@491.52e6")],
            [{},                                      pytest.param(False,     491.52e6, 0,      "",         491.52e6, "0,1",      64,             id="1x100GbE-2xTX@491.52e6")],
            [{},                                      pytest.param(False,     491.52e6, 491.52e6, "0,1",     0,        "",        64,             id="1x100GbE-2xRX@491.52e6")],
            [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(True,      491.52e6, 491.52e6, "0,1,2,3", 491.52e6, "0,1,2,3", 64,             id="2x100GbE-4xTRX@491.52e6", marks=pytest.mark.xfail)],
            [{},                                      pytest.param(True,      491.52e6, 0,       "",         491.52e6, "0,1,2,3", 64,             id="2x100GbE-4xTX@491.52e6")],
            [{},                                      pytest.param(True,      491.52e6, 491.52e6, "0,1,2,3", 0,        "",        64,             id="2x100GbE-4xRX@491.52e6")],
            # fmt: on
        ]

    if dut_fpga.upper() == "UC_200":
        test_cases = [
            # fmt: off
            # Test Lengths                                         dual_sfp    rate      rx_rate  rx_channels tx_rate  tx_channels tx_sample_align test case ID                # noqa: W505
            [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(False,      250e6,   250e6,    "0,1,2",    250e6,  "0,1,2",     64,             id="1x100GbE-3xTRX@250e6")],
            [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(False,      250e6,   0,        "",         250e6,  "0,1,2,3",   64,             id="1x100GbE-4xTX@250e6")],
            [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(False,      250e6,   250e6,    "0,1,2,3",  0,      "",          64,             id="1x100GbE-4xRX@250e6")],
            # fmt: on
        ]

    argvalues = test_length_utils.select_test_cases_by_length(test_length, test_cases)
    metafunc.parametrize(ARGNAMES_DUAL_SFP, argvalues)

    fast_params = test_length_utils.test_length_params(iterations=10, duration=30)
    stress_params = test_length_utils.test_length_params(iterations=2, duration=600)
    parametrize_test_length(metafunc, test_length, fast_params, stress_params)


def _generate_x440_test_cases(metafunc, test_length, dut_fpga):
    # Test Cases chosen from published spec: https://kb.ettus.com/X440#100_Gigabit_Ethernet
    # Note some cases reduced number of channels on Tx 450 for and rate reduced for CG_1600 Tx
    if dut_fpga.upper() == "CG_400":
        test_cases = [
            # fmt: off
            # Test Lengths                                         dual_sfp  rate       rx_rate  rx_channels       tx_rate   tx_channels        tx_sample_align test case ID # noqa: W505
            # ---------------------------------------------------------------------------------------------------------------------------------------------- # noqa: W505
            [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(True,     500e6,    500e6,    "0,1,2,3,4,5",     0,        "",               None,           id="2x100GbE-6xRX@500e6")],
            [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(True,     500e6,    0,        "",                500e6,    "0,1,2,3,4,5",    None,           id="2x100GbE-6xTX@500e6")],
            [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(True,     450e6,    0,        "",                450e6,    "0,1,2,3,4,5",    None,           id="2x100GbE-6xTX@450e6")],
            [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(True,     500e6,    500e6,    "0,1,2,3",         500e6,    "0,1,2,3",        None,           id="2x100GbE-4xTRX@500e6")],
            [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(True,     250e6,    250e6,    "0,1,2,3,4,5,6,7", 250e6,    "0,1,2,3,4,5,6,7",None,           id="2x100GbE-8xTRX@250e6")],
            # fmt: on
        ]
    if dut_fpga.upper() == "CG_1600":
        test_cases = [
            # fmt: off
            # Test Lengths                                         dual_sfp  rate       rx_rate   rx_channels tx_rate   tx_channels tx_sample_align test case ID # noqa: W505
            # ----------------------------------------------------------------------------------------------------------------------------------- # noqa: W505
            [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(True,     1000e6,    1000e6,   "0,1",      0,        "",         None,           id="2x100GbE-2xRX@1000e6")],
            [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(True,     1000e6,    0,        "",         1000e6,   "0,1",      None,           id="2x100GbE-2xTX@1000e6")],
            [{Test_Length_Stress, Test_Length_Smoke}, pytest.param(True,     1000e6,    1000e6,   "0,1",      1000e6,   "0,1",      None,           id="2x100GbE-2xTRX@1000e6")],
            # fmt: on
        ]

    argvalues = test_length_utils.select_test_cases_by_length(test_length, test_cases)
    metafunc.parametrize(ARGNAMES_DUAL_SFP, argvalues)

    fast_params = test_length_utils.test_length_params(iterations=10, duration=30)
    stress_params = test_length_utils.test_length_params(iterations=2, duration=600)
    parametrize_test_length(metafunc, test_length, fast_params, stress_params)


def pytest_generate_tests(metafunc):
    """Generate parameterized pytest test cases."""
    dut_type = metafunc.config.getoption("dut_type")
    dut_fpga = metafunc.config.getoption("dut_fpga")
    test_length = metafunc.config.getoption("test_length")

    metafunc.parametrize("dut_type", [dut_type])

    if dut_type.lower() == "b210":
        argvalues_dpdk = [
            #            use_dpdk  test case ID  marks
            pytest.param(
                False,
                id="NO DPDK",
            )
        ]
    else:
        argvalues_dpdk = [
            #            use_dpdk  test case ID  marks
            pytest.param(True, id="DPDK", marks=pytest.mark.dpdk),
            pytest.param(
                False,
                id="NO DPDK",
            ),
        ]
    metafunc.parametrize("use_dpdk", argvalues_dpdk)

    if dut_type.lower() == "n310":
        _generate_n310_test_cases(metafunc, test_length)
    elif dut_type.lower() == "n320":
        _generate_n320_test_cases(metafunc, test_length)
    elif dut_type.lower() == "b210":
        _generate_b210_test_cases(metafunc, test_length)
    elif dut_type.lower() == "e320":
        _generate_e320_test_cases(metafunc, test_length)
    elif dut_type.lower() == "x310":
        _generate_x310_test_cases(metafunc, test_length)
    elif dut_type.lower() == "x310_twinrx":
        _generate_x310_twinrx_test_cases(metafunc, test_length)
    elif dut_type.lower() == "x410":
        _generate_x410_test_cases(metafunc, test_length, dut_fpga)
    elif dut_type.lower() == "x440":
        _generate_x440_test_cases(metafunc, test_length, dut_fpga)


def test_streaming(
    pytestconfig,
    dut_type,
    use_dpdk,
    dual_sfp,
    rate,
    rx_rate,
    rx_channels,
    tx_rate,
    tx_channels,
    tx_sample_align,
    iterations,
    duration,
):
    """Run actual streaming tests by invoking benchmark_rate executable."""
    benchmark_rate_path = Path(pytestconfig.getoption("uhd_build_dir")) / "examples/benchmark_rate"

    device_args = ""

    # construct device args string
    if dut_type.lower() in ["n310", "n320", "e320", "b210", "x440"]:
        device_args += f"master_clock_rate={rate},"

    # mpm reboot on x440 is for spurrious RF performance,
    # these tests do not care about RF performance
    if dut_type.lower() == "x440":
        device_args += f"skip_mpm_reboot=1,"

    if dut_type == "B210":
        device_args += f"name={pytestconfig.getoption('name')},"
    else:
        device_args += f"addr={pytestconfig.getoption('addr')},"

    if dual_sfp:
        device_args += f"second_addr={pytestconfig.getoption('second_addr')},"

    if use_dpdk:
        device_args += f"use_dpdk=1,"
        try:
            mgmt_addr = pytestconfig.getoption("mgmt_addr")
            if mgmt_addr:
                device_args += f"mgmt_addr={mgmt_addr},"
        except Exception:
            pass

    try:
        num_recv_frames = pytestconfig.getoption("num_recv_frames")
        if num_recv_frames:
            device_args += f"num_recv_frames={num_recv_frames},"
    except Exception:
        pass

    try:
        num_send_frames = pytestconfig.getoption("num_send_frames")
        if num_send_frames:
            device_args += f"num_send_frames={num_send_frames},"
    except Exception:
        pass

    print("Constructed device_args: " + device_args)

    # construct benchmark_rate params dictionary
    benchmark_rate_params = {
        "args": device_args,
        "duration": duration,
        "priority": "high",
    }

    if rx_channels:
        benchmark_rate_params["rx_rate"] = rx_rate
        benchmark_rate_params["rx_channels"] = rx_channels

    if tx_channels:
        benchmark_rate_params["tx_rate"] = tx_rate
        benchmark_rate_params["tx_channels"] = tx_channels

    if tx_sample_align:
        benchmark_rate_params["tx_sample_align"] = tx_sample_align

    # Run X410 streaming tests in multi_streamer mode and high thread priority
    # since those settings allow for best performance.
    if dut_type.lower() == "x410" or dut_type.lower() == "x440":
        benchmark_rate_params["multi_streamer"] = 1
        benchmark_rate_params["priority"] = "high"
        dut_fpga = pytestconfig.getoption("dut_fpga")
        if dut_fpga.upper() == "UC_200":
            # TODO: Remove this delay workaround when IO errors on multi_streamer
            # config are resolved for UC_200.
            benchmark_rate_params["tx_delay"] = 1.5
            benchmark_rate_params["rx_delay"] = 0.5
        if dut_fpga.upper() == "CG_400" or dut_fpga.upper() == "CG_1600":
            # TODO: Remove this delay workaround when IO errors on multi_streamer
            # config are resolved for UC_200.
            benchmark_rate_params["tx_delay"] = 2
            benchmark_rate_params["rx_delay"] = 2

    # run benchmark rate
    print()
    results = batch_run_benchmark_rate.run(benchmark_rate_path, iterations, benchmark_rate_params)
    stats = batch_run_benchmark_rate.calculate_stats(results)
    print(batch_run_benchmark_rate.get_summary_string(stats, iterations, benchmark_rate_params))

    # compare results against thresholds
    # TODO: Have non adhoc better thresholds.
    dropped_samps_threshold = 50
    overruns_threshold = 50
    rx_timeouts_threshold = 50
    rx_seq_err_threshold = 50

    underruns_threshold = 50
    tx_timeouts_threshold = 50
    tx_seq_err_threshold = 50

    late_cmds_threshold = 50

    # TODO: define custom failed assertion explanations to avoid extra output
    # https://docs.pytest.org/en/6.2.x/assert.html#defining-your-own-explanation-for-failed-assertions

    if rx_channels:
        assert (
            stats.avg_vals.dropped_samps <= dropped_samps_threshold
        ), f"""Number of dropped samples exceeded threshold.
                Expected dropped samples: <= {dropped_samps_threshold}
                Actual dropped samples:      {stats.avg_vals.dropped_samps}"""
        assert (
            stats.avg_vals.rx_timeouts <= rx_timeouts_threshold
        ), f"""Number of rx timeouts exceeded threshold.
                Expected rx timeouts: <= {rx_timeouts_threshold}
                Actual rx timeouts:      {stats.avg_vals.rx_timeouts}"""
        assert (
            stats.avg_vals.rx_seq_errs <= rx_seq_err_threshold
        ), f"""Number of rx sequence errors exceeded threshold.
                Expected rx sequence errors: <= {rx_seq_err_threshold}
                Actual rx sequence errors:      {stats.avg_vals.rx_seq_errs}"""
        if not stats.avg_vals.overruns <= overruns_threshold:
            overrun_error_text = (
                f"Number of overruns exceeded threshold.\n"
                f"Expected overruns: <= {overruns_threshold}\n"
                f"Actual overruns:      {stats.avg_vals.overruns}\n"
            )
            if not use_dpdk:
                pytest.xfail(overrun_error_text)
            else:
                assert False, overrun_error_text

    if tx_channels:
        assert (
            stats.avg_vals.tx_timeouts <= tx_timeouts_threshold
        ), f"""Number of tx timeouts exceeded threshold.
                Expected tx timeouts: <= {tx_timeouts_threshold}
                Actual tx timeouts:      {stats.avg_vals.tx_timeouts}"""
        assert (
            stats.avg_vals.tx_seq_errs <= tx_seq_err_threshold
        ), f"""Number of tx sequence errors exceeded threshold.
                Expected tx sequence errors: <= {tx_seq_err_threshold}
                Actual tx sequence errors:      {stats.avg_vals.tx_seq_errs}"""
        if not stats.avg_vals.underruns <= underruns_threshold:
            underrun_error_text = (
                f"Number of underruns exceeded threshold.\n"
                f"Expected underruns: <= {underruns_threshold}\n"
                f"Actual underruns:      {stats.avg_vals.underruns}\n"
            )
            if not use_dpdk:
                pytest.xfail(underrun_error_text)
            else:
                assert False, underrun_error_text

    assert (
        stats.avg_vals.late_cmds <= late_cmds_threshold
    ), f"""Number of late commands exceeded threshold.
            Expected late commands: <= {late_cmds_threshold}
            Actual late commands:      {stats.avg_vals.late_cmds}"""
