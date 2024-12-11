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
  wire is_random_rsc_dat;
  wire is_random_triosy_lz;
  wire valid_rsc_dat;
  wire valid_triosy_lz;
  wire epsilon_triosy_lz;

  // 使用 ui_in[0] 做为 epsilon_rsc_dat
  wire epsilon_rsc_dat = ui_in[0];

  monobit monobit_inst (
      .clk                  (clk),
      .rst                  (~rst_n), // rst 为有源高，故使用~rst_n
      .is_random_rsc_dat    (is_random_rsc_dat),
      .is_random_triosy_lz  (is_random_triosy_lz),
      .valid_rsc_dat        (valid_rsc_dat),
      .valid_triosy_lz      (valid_triosy_lz),
      .epsilon_rsc_dat      (epsilon_rsc_dat),
      .epsilon_triosy_lz    (epsilon_triosy_lz)
  );

  // 输出分配
  // uo_out:
  // Bit 0 - is_random_rsc_dat
  // Bit 1 - valid_rsc_dat
  // Bit 2 - is_random_triosy_lz
  // Bit 3 - valid_triosy_lz
  // Bit 4 - epsilon_triosy_lz
  // 其余位清0
  assign uo_out = {3'b000, epsilon_triosy_lz, valid_triosy_lz, is_random_triosy_lz, valid_rsc_dat, is_random_rsc_dat};

  // 不使用 uio_out 和 uio_oe
  assign uio_out = 8'b00000000;
  assign uio_oe  = 8'b00000000;

  // 将未使用信号连接以避免综合警告
  wire _unused = &{ena, uio_in, 1'b0};

endmodule
