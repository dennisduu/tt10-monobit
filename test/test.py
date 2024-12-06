# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
import random

@cocotb.test()
async def test_project_constrained_random(dut):
    """Constrained random test for tt_um_example design."""

    # Create a 10us period clock on dut.clk
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Apply reset
    dut._log.info("Applying reset")
    dut.ena.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    dut.ena.value = 1

    # Wait after reset
    await ClockCycles(dut.clk, 10)

    # Define your constraints:
    # For example:
    #  - ui_in must be even
    #  - uio_in must be greater than ui_in
    #  - both are 8-bit values
    # You can choose your own constraints as needed for your logic.
    NUM_TESTS = 100

    for i in range(NUM_TESTS):
        # Generate random values and apply constraints:
        # Start by generating random values until they satisfy constraints
        # Constraint: ui_in is even, and uio_in > ui_in
        ui_candidate = random.randint(0, 255)
        # ensure ui_in is even
        if ui_candidate % 2 != 0:
            ui_candidate += 1
            if ui_candidate > 255:
                ui_candidate = 254  # wrap around if we went out of range

        # For uio_in, let's say uio_in must be greater than ui_in
        # We pick a random value between ui_candidate and 255
        uio_candidate = random.randint(ui_candidate, 255)

        dut.ui_in.value = ui_candidate
        dut.uio_in.value = uio_candidate

        dut._log.info(f"Test {i}: ui_in={ui_candidate}, uio_in={uio_candidate}")

        # Wait for output to settle on next clock cycle
        await ClockCycles(dut.clk, 1)

        # Now implement a check based on expected behavior:
        # For demonstration, if your DUT just sums ui_in and uio_in:
        expected = ui_candidate + uio_candidate
        # Since both are 8-bit, if there's wrapping logic, you may want to mod by 256:
        expected = expected & 0xFF

        # Check the output
        got = dut.uo_out.value.integer
        assert got == expected, f"Test {i} Failed: ui_in={ui_candidate}, uio_in={uio_candidate}, expected={expected}, got={got}"

    dut._log.info("Constrained random test completed successfully.")
