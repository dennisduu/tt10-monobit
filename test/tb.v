`default_nettype none
`timescale 1ns / 1ps

module tb ();

  // Dump the signals to a VCD file
  initial begin
    $dumpfile("tb.vcd");
    $dumpvars(0, tb);
    #1;
  end

  // Testbench signals
  reg clk;
  reg rst_n;
  reg ena;
  reg [7:0] ui_in;
  reg [7:0] uio_in;
  wire [7:0] uo_out;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;

`ifdef GL_TEST
  wire VPWR = 1'b1;
  wire VGND = 1'b0;
`endif

  // Instantiate the DUT (Device Under Test)
  tt_um_monobit user_project (
`ifdef GL_TEST
      .VPWR(VPWR),
      .VGND(VGND),
`endif
      .ui_in (ui_in),     // Dedicated inputs
      .uo_out(uo_out),    // Dedicated outputs
      .uio_in(uio_in),    // IOs: Input path
      .uio_out(uio_out),  // IOs: Output path
      .uio_oe(uio_oe),    // IOs: Enable path (active high)
      .ena(ena),          // enable
      .clk(clk),          // clock
      .rst_n(rst_n)       // reset (active low)
  );

  // Clock generation
  initial begin
    clk = 0;
    forever #5 clk = ~clk;  // 10ns period, 100MHz approx.
  end

  // Initialize signals
  initial begin
    ena   = 0;
    rst_n = 0;
    ui_in = 8'h00;
    uio_in = 8'h00;

    // Wait a bit, then release reset
    #100;
    rst_n = 1;
    ena   = 1;

    // The actual stimulus is provided by the cocotb test.py
    // So we don't drive more signals here. cocotb will drive them.
  end

endmodule
