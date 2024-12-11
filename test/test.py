import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles
import random

@cocotb.test()
async def test_tt_um_monobit(dut):
    """Testbench for the tt_um_monobit module with 128-bit input."""

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
        # Generate constrained random input patterns
        # Example: 3:7, 4:6, 5:5 ratios of 1s to 0s
        num_ones = random.choice([38, 51, 64])  # Adjust these values for different ratios
        bits = [1] * num_ones + [0] * (128 - num_ones)
        random.shuffle(bits)  # Shuffle to randomize the positions of 1s and 0s

        # Convert bits to a single integer for ui_in
        epsilon_input = int("".join(map(str, bits)), 2)
        dut.ui_in.value = epsilon_input

        dut._log.info(f"Test {i}: epsilon_input={bin(epsilon_input)}")

        # Wait for one clock cycle
        await ClockCycles(dut.clk, 1)

        # Count number of 1s and 0s in the input
        count_ones = bits.count(1)
        count_zeros = bits.count(0)
        diff = abs(count_ones - count_zeros)

        # Capture output signals
        is_random = dut.uo_out.value & 0b1  # Bit 0
        valid = (dut.uo_out.value >> 1) & 0b1  # Bit 1

        dut._log.info(
            f"Output: is_random={is_random}, valid={valid}, count_ones={count_ones}, count_zeros={count_zeros}, diff={diff}"
        )

        # Perform checks
        if valid:
            expected_is_random = 1 if diff <= 29 else 0
            assert is_random == expected_is_random, (
                f"Mismatch: expected is_random={expected_is_random}, got {is_random}"
            )

    dut._log.info("All tests completed successfully.")
