import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles
import random

@cocotb.test()
async def test_monobit_serial(dut):
    """Testbench for monobit module with serial 128-bit input."""

    # Create a 10 ns period clock (100 MHz) on dut.clk
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Apply reset
    dut._log.info("Applying reset")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1

    NUM_TESTS = 10  # Number of test iterations

    for test_idx in range(NUM_TESTS):
        # Generate a 128-bit random input
        serial_data = [random.randint(0, 1) for _ in range(128)]

        count_ones = 0
        count_zeros = 0

        for bit_idx, bit in enumerate(serial_data):
            dut.epsilon_rsc_dat.value = bit
            await RisingEdge(dut.clk)

            # Count 1s and 0s for validation
            if bit == 1:
                count_ones += 1
            else:
                count_zeros += 1

        # Wait for the outputs to stabilize
        await ClockCycles(dut.clk, 5)

        # Calculate the expected result
        difference = abs(count_ones - count_zeros)
        expected_is_random = 1 if difference <= 29 else 0

        # Capture and log the output
        is_random = dut.is_random_rsc_dat.value
        valid = dut.valid_rsc_dat.value

        dut._log.info(
            f"Test {test_idx}: Count(1s)={count_ones}, Count(0s)={count_zeros}, Difference={difference}, "
            f"Expected is_random={expected_is_random}, Actual is_random={is_random}, Valid={valid}"
        )

        # Perform assertions
        assert valid == 1, "Output valid signal is not asserted!"
        assert is_random == expected_is_random, (
            f"Mismatch: Expected is_random={expected_is_random}, Got is_random={is_random}"
        )

    dut._log.info("All tests completed successfully.")
