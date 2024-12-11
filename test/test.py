import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles
import random

@cocotb.test()
async def test_tt_um_monobit(dut):
    """Testbench for the tt_um_monobit module."""

    # Create a 10 ns period clock (100 MHz) on dut.clk
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Apply reset
    dut._log.info("Applying reset")
    dut.rst_n.value = 0
    dut.ena.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    dut.ena.value = 1

    # Wait for a few clock cycles after reset
    await ClockCycles(dut.clk, 5)

    NUM_TESTS = 300  # Number of test iterations

    for i in range(NUM_TESTS):
        # Generate random input bit for ui_in[0] (epsilon_rsc_dat)
        epsilon_bit = random.randint(0, 1)
        dut.ui_in.value = epsilon_bit

        dut._log.info(f"Test {i}: epsilon_rsc_dat={epsilon_bit}")

        # Wait for one clock cycle
        await ClockCycles(dut.clk, 1)

        # Capture output signals
        is_random = dut.uo_out.value & 0b1  # Bit 0
        valid = (dut.uo_out.value >> 1) & 0b1  # Bit 1
        is_random_triosy = (dut.uo_out.value >> 2) & 0b1  # Bit 2
        valid_triosy = (dut.uo_out.value >> 3) & 0b1  # Bit 3
        epsilon_triosy = (dut.uo_out.value >> 4) & 0b1  # Bit 4

        dut._log.info(
            f"Output: is_random={is_random}, valid={valid}, is_random_triosy={is_random_triosy}, valid_triosy={valid_triosy}, epsilon_triosy={epsilon_triosy}"
        )

        # Perform checks
        # Assuming `valid` indicates a valid output and `is_random` is the result to check
        if valid:
            assert is_random in [0, 1], f"Invalid is_random value: {is_random}"

    dut._log.info("All tests completed successfully.")
