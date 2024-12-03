# test_monobit.py

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
import random

@cocotb.test()
async def monobit_test(dut):
    """Test the monobit module."""

    # initialization
    dut.clk <= 0
    dut.rst_n <= 0
    dut.ena <= 0
    dut.ui_in <= 0
    dut.uio_in <= 0
    dut.uio_oe <= 0xFF 

    # generate clock
    clock = Clock(dut.clk, 10, units="ns")  # 10ns clock period
    cocotb.fork(clock.start())

    # reset
    await Timer(20, units='ns')
    dut.rst_n <= 1
    await RisingEdge(dut.clk)
    dut.ena <= 1

    # set uio_oe[0] as input
    dut.uio_oe[0] <= 0 
    await RisingEdge(dut.clk)

    # prepare for the test parameter
    N_TESTS = 65536
    bit_stream = []
    for i in range(N_TESTS):
        if i > 3:
            rnd = i % 2
        else:
            rnd = 0
        bit_stream.append(rnd)

    # send bitstream to the DUT
    for bit in bit_stream:
        dut.uio_in[0] <= bit
        await RisingEdge(dut.clk)

    # waiting for the final output valid
    for _ in range(10):
        await RisingEdge(dut.clk)

    # read result
    is_random = dut.uo_out[0].value.integer  # set uo_out[0] as is_random
    valid = dut.uo_out[1].value.integer      # set uo_out[1] as valid

    # print result
    cocotb.log.info(f"valid: {valid} \t random: {is_random}")

    # assert check
    if valid:
        if is_random:
            cocotb.log.info("The bit stream passed the monobit test.")
        else:
            cocotb.log.info("The bit stream failed the monobit test.")
    else:
        cocotb.log.warning("The result is not valid yet.")
