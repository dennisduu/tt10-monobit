import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles
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

    # Reset the design
    dut.rst <= 1
    await ClockCycles(dut.clk, 5)  # Hold reset for 5 clock cycles
    dut.rst <= 0

    # Configuration for the test
    SEQUENCE_LENGTH = 128  # Each sequence contains 128 bits
    corner_cases = [
        [1] * SEQUENCE_LENGTH,  # All 1s
        [0] * SEQUENCE_LENGTH   # All 0s
    ]
    random_sequences = [[random.randint(0, 1) for _ in range(SEQUENCE_LENGTH)] for _ in range(10)]

    # Combine corner cases and random sequences
    test_sequences = corner_cases + random_sequences

    # Run tests for all sequences
    for idx, sequence in enumerate(test_sequences):
        dut._log.info(f"Testing sequence {idx + 1}/{len(test_sequences)}")

        # Apply the sequence as an array
        for bit in sequence:
            dut.epsilon_rsc_dat <= bit
            await RisingEdge(dut.clk)

        # Wait for the result to be valid
        await ClockCycles(dut.clk, 1)

        # Capture outputs
        is_random = int(dut.is_random_rsc_dat.value)
        valid = int(dut.valid_rsc_dat.value)

        # Validate outputs
        assert valid == 1, f"Sequence {idx + 1}: Valid signal was not asserted."

        if idx == 0:  # All 1s
            assert is_random == 0, f"Failed for all 1s. Expected 0, got {is_random}."
        elif idx == 1:  # All 0s
            assert is_random == 0, f"Failed for all 0s. Expected 0, got {is_random}."
        else:
            dut._log.info(f"Random sequence result: {is_random}")

        dut._log.info(f"Sequence {idx + 1} passed with is_random={is_random}")

    dut._log.info("All tests completed successfully.")
