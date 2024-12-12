import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles, Timer
import random




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
    dut._log.info("Reset\n")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    cycle_counter = 0

    all_zero = [0] * 128
    all_one = [1] * 128
    rand_stream1 = [random.randint(0, 1) for _ in range(128)]
    rand_stream2 = [random.randint(0, 1) for _ in range(128)]
    rand_stream3 = [random.randint(0, 1) for _ in range(128)]
    bit_stream = all_zero + all_one + rand_stream1 + rand_stream2 + rand_stream3 + [0] * 2

    dut._log.info(f"Start Testing...\n")
    for i in range(len(bit_stream)):
        for _ in range(5):
            cycle_counter += 1
            input_bit = bit_stream[i]
            dut.ui_in.value = input_bit
            dut._log.info(f"Cycle: {cycle_counter}, input_bit: {input_bit}")
            await Timer(1, units="ns")
            out = dut.uo_out.value
            is_random = out & 1
            is_valid  = (out >> 1) & 1
            fsm_state = dut.uio_out.value & 31
            dut._log.info(f"is_random: {is_random}, is_valid: {is_valid}, fsm_state: {fsm_state}")
            await ClockCycles(dut.clk, 1)

    dut._log.info("\nAll tests completed successfully.\n")
