import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles

@cocotb.test()
async def test_monobit_hls_style(dut):
    """
    Test the monobit design in a style similar to the HLS testbench, running multiple tests with deterministic inputs.
    """
    # Create a 10ns clock (100 MHz)
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset the design
    dut.rst <= 1
    await ClockCycles(dut.clk, 5)  # Hold reset for 5 clock cycles
    dut.rst <= 0

    N_TESTS = 65536  # Number of tests to run

    for i in range(N_TESTS):
        # Generate deterministic input sequence
        rnd = 0 if i <= 3 else i % 2

        # Apply input to the DUT
        dut.epsilon_rsc_dat <= rnd
        await RisingEdge(dut.clk)

        # Wait for the result to be valid
        await ClockCycles(dut.clk, 1)

        # Capture outputs
        is_random = int(dut.is_random_rsc_dat.value)
        valid = int(dut.valid_rsc_dat.value)

        # Log outputs
        dut._log.info(f"Test {i + 1}: rnd={rnd}, valid={valid}, is_random={is_random}")

        # Ensure valid signal is asserted
        assert valid == 1, f"Test {i + 1}: Valid signal was not asserted."

    dut._log.info("All HLS-style tests completed successfully.")
