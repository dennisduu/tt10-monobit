/*
 * Copyright (c) 2024 Dennis Du & Rick Gao
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_monobit (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (1=output)
    input  wire       ena,      // always 1 when powered
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // Monobit signals
  
  wire epsilon_rsc_dat;      // Input bit flow

  wire is_random_rsc_dat;   // Output is random
  wire is_random_triosy_lz;

  wire valid_rsc_dat;       // Output is valid
  wire valid_triosy_lz;
  
  wire epsilon_triosy_lz;


  // use ui_in[0] as epsilon_rsc_dat
  wire epsilon_rsc_dat = ui_in[0];


  monobit monobit_inst (
      .clk                  (clk),
      .rst                  (~rst_n),               // Invert rst_n to rst 
      .is_random_rsc_dat    (is_random_rsc_dat),
      .is_random_triosy_lz  (is_random_triosy_lz),
      .valid_rsc_dat        (valid_rsc_dat),
      .valid_triosy_lz      (valid_triosy_lz),
      .epsilon_rsc_dat      (epsilon_rsc_dat),
      .epsilon_triosy_lz    (epsilon_triosy_lz)
  );

  // output port：monobit result to uo_out
  // Bit 0 - is_random_rsc_dat
  // Bit 1 - valid_rsc_dat
  // Bit 4:2 - Zero
  // Bit 5 - is_random_triosy_lz
  // Bit 6 - valid_triosy_lz
  // Bit 7 - epsilon_triosy_lz
  
  assign uo_out[0] = is_random_rsc_dat;
  assign uo_out[1] = valid_rsc_dat;

  assign uo_out[4:2] = 3'b000;

  assign uo_out[5] = is_random_triosy_lz;
  assign uo_out[6] = valid_triosy_lz;
  assign uo_out[7] = epsilon_triosy_lz;

  

  // NOT USING uio_out and uio_oe
  assign uio_out = 8'b00000000;
  assign uio_oe  = 8'b00000000;

  // list all unused port avoid warning
  wire _unused = &{ena, uio_in, 1'b0};

endmodule
