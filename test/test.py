import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer

@cocotb.test()
async def test_monobit(dut):
    """Simple cocotb testbench for the monobit module."""

    # Start a clock
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())  # 100 MHz clock

    # Reset the DUT
    dut.rst_n.value = 0
    dut.ena.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # Wait a bit before releasing reset
    for _ in range(10):
        await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    dut.ena.value = 1

    # Wait a cycle for stable state
    await RisingEdge(dut.clk)

    # Now we will drive some patterns to epsilon_rsc_dat which is ui_in[0]
    # and observe the outputs.
    # According to the code, uo_out bits are assigned as:
    # Bit 0 - is_random_rsc_dat
    # Bit 1 - valid_rsc_dat
    # Bit 2 - is_random_triosy_lz
    # Bit 3 - valid_triosy_lz
    # Bit 4 - epsilon_triosy_lz
    # The rest are 0.

    # Let's toggle ui_in[0] (epsilon_rsc_dat) and run for several cycles
    # to see how the output evolves.
    for toggle_val in [0, 1, 0, 1, 0]:
        dut.ui_in.value = toggle_val
        # Let the design run for a number of cycles to observe the FSM
        for _ in range(100):
            await RisingEdge(dut.clk)
            # Print outputs for debug
            is_random        = dut.uo_out.value.integer & 0x01
            valid            = (dut.uo_out.value.integer >> 1) & 0x01
            is_random_lz     = (dut.uo_out.value.integer >> 2) & 0x01
            valid_lz         = (dut.uo_out.value.integer >> 3) & 0x01
            epsilon_triosy_lz= (dut.uo_out.value.integer >> 4) & 0x01

            # Debug printing
            dut._log.info(f"ui_in[0]={toggle_val} | uo_out={dut.uo_out.value.binstr} | "
                          f"is_random={is_random} valid={valid} "
                          f"is_random_lz={is_random_lz} valid_lz={valid_lz} "
                          f"epsilon_triosy_lz={epsilon_triosy_lz}")

    # Simple checks (not rigorous): since the design uses an FSM and accumulates bits,
    # after many cycles, `valid_rsc_dat` and `is_random_rsc_dat` should eventually
    # become high once enough bits are processed. For demonstration:
    if valid == 0:
        dut._log.warning("At end of test, valid_rsc_dat is still 0. Consider extending the simulation or verifying logic.")
    else:
        dut._log.info("valid_rsc_dat is high as expected after sufficient cycles.")
