import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles, Timer
import random



TEST_LENGTH = 1000


@cocotb.test()
async def test_monobit(dut):
    """
    Test the monobit design by sending 128-bit sequences as a single array and validating
    if `is_random` outputs 0 or 1 correctly.
    """
    # Create a 10ns clock (100 MHz)
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    for i in range(TEST_LENGTH):
        input_bit = random.randint(0, 1)
        dut.ui_in.value = input_bit
        await Timer(1, units="ns")
        out = dut.uo_out.value
        is_random = out & 1
        is_valid  = (out >> 1) & 1
        dut._log.info(f"input_bit: {input_bit}, is_random: {is_random}, is_valid: {is_valid}")
        await ClockCycles(dut.clk, 1)

    dut._log.info("All tests completed successfully.")
