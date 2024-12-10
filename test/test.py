import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles
import random

@cocotb.test()
async def test_monobit(dut):
    """
    Test the monobit design for corner cases (all 1s and all 0s) and random sequences.
    Validate results after 128 cycles.
    """
    # Create a 10ns clock (100 MHz)
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset the design
    dut.rst <= 1
    dut.epsilon_rsc_dat <= 0
    await ClockCycles(dut.clk, 5)  # Hold reset for 5 clock cycles
    dut.rst <= 0

    # Configuration for the test
    NUM_SEQUENCES = 10  # Number of sequences to test
    SEQUENCE_LENGTH = 128  # Each sequence contains 128 bits
    corner_cases = [
        [1] * SEQUENCE_LENGTH,  # All 1s
        [0] * SEQUENCE_LENGTH   # All 0s
    ]
    random_sequences = [[random.randint(0, 1) for _ in range(SEQUENCE_LENGTH)] for _ in range(NUM_SEQUENCES)]

    # Combine corner cases and random sequences
    test_sequences = corner_cases + random_sequences

    # Python storage for results
    results = []

    for idx, sequence in enumerate(test_sequences):
        dut._log.info(f"Testing sequence {idx + 1}/{len(test_sequences)}: {sequence}")

        # Apply the sequence bit by bit
        for bit in sequence:
            dut.epsilon_rsc_dat <= bit
            await RisingEdge(dut.clk)

        # Wait for outputs to settle after 128 cycles
        await ClockCycles(dut.clk, 1)

        # Capture the outputs
        is_random = int(dut.is_random_rsc_dat.value)
        valid = int(dut.valid_rsc_dat.value)

        # Log the results
        result = {
            "sequence": sequence,
            "is_random": is_random,
            "valid": valid
        }
        results.append(result)

        # Check if the result is valid
        if valid != 1:
            raise AssertionError(f"Sequence {idx + 1} did not produce a valid result.")

        # Log corner cases specific checks
        if idx == 0:  # All 1s
            expected = 0  # Non-random (sum = 128)
            assert is_random == expected, f"Failed for all 1s. Expected {expected}, got {is_random}."
        elif idx == 1:  # All 0s
            expected = 0  # Non-random (sum = -128)
            assert is_random == expected, f"Failed for all 0s. Expected {expected}, got {is_random}."

    # Log results for random sequences
    dut._log.info("Random sequence results:")
    for idx, res in enumerate(results[2:]):  # Skip corner cases
        dut._log.info(f"Sequence {idx + 1}: {res}")

    # Output the results
    with open("test_results.txt", "w") as f:
        for result in results:
            f.write(f"{result}\n")

    dut._log.info("Test completed successfully.")
