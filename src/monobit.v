module monobit_core_core_fsm (
  clk, rst, fsm_output
);
  input clk;
  input rst;
  output [4:0] fsm_output;
  reg [4:0] fsm_output;

  parameter
    main_C_0 = 3'd0,
    main_C_1 = 3'd1,
    main_C_2 = 3'd2,
    main_C_3 = 3'd3,
    main_C_4 = 3'd4;

  reg [2:0] state_var;
  reg [2:0] state_var_NS;

  always @(*)
  begin : monobit_core_core_fsm_1
    case (state_var)
      main_C_1 : begin
        fsm_output = 5'b00010;
        state_var_NS = main_C_2;
      end
      main_C_2 : begin
        fsm_output = 5'b00100;
        state_var_NS = main_C_3;
      end
      main_C_3 : begin
        fsm_output = 5'b01000;
        state_var_NS = main_C_4;
      end
      main_C_4 : begin
        fsm_output = 5'b10000;
        state_var_NS = main_C_0;
      end
      default : begin
        fsm_output = 5'b00001;
        state_var_NS = main_C_1;
      end
    endcase
  end

  always @(posedge clk) begin
    if ( rst ) begin
      state_var <= main_C_0;
    end
    else begin
      state_var <= state_var_NS;
    end
  end

endmodule

module monobit_core (
  clk, rst, is_random_rsc_dat, valid_rsc_dat,
      epsilon_rsc_dat
);
  input clk;
  input rst;
  output is_random_rsc_dat;
  output valid_rsc_dat;
  input epsilon_rsc_dat;

  reg is_random_rsci_idat;
  reg valid_rsci_idat;
  reg [6:0] bit_count_sva;
  reg [7:0] sum_sva;
  wire [4:0] fsm_output;

  monobit_core_core_fsm monobit_core_core_fsm_inst (
      .clk(clk),
      .rst(rst),
      .fsm_output(fsm_output)
    );

  always @(posedge clk) begin
    if ( rst ) begin
      valid_rsci_idat <= 1'b0;
    end
    else if ( fsm_output[0] ) begin
      valid_rsci_idat <= (bit_count_sva == 7'b1111111);
    end
  end

  always @(posedge clk) begin
    if ( rst ) begin
      is_random_rsci_idat <= 1'b0;
    end
    else if ( fsm_output[0] ) begin
      is_random_rsci_idat <= (sum_sva >= -8'd29 && sum_sva <= 8'd29) && (bit_count_sva == 7'b1111111);
    end
  end

  always @(posedge clk) begin
    if ( rst ) begin
      bit_count_sva <= 7'b0000000;
    end
    else if ( fsm_output[0] ) begin
      bit_count_sva <= bit_count_sva + 1;
    end
  end

  always @(posedge clk) begin
    if ( rst ) begin
      sum_sva <= 8'b00000000;
    end
    else if ( fsm_output[0] ) begin
      if (bit_count_sva == 7'b1111111) begin
        sum_sva <= 8'b00000000;
      end else begin
        sum_sva <= sum_sva + (epsilon_rsc_dat ? 8'd1 : -8'd1);
      end
    end
  end

  assign is_random_rsc_dat = is_random_rsci_idat;
  assign valid_rsc_dat = valid_rsci_idat;

endmodule

module monobit (
  clk, rst, is_random_rsc_dat, valid_rsc_dat,
      epsilon_rsc_dat
);
  input clk;
  input rst;
  output is_random_rsc_dat;
  output valid_rsc_dat;
  input epsilon_rsc_dat;

  monobit_core monobit_core_inst (
      .clk(clk),
      .rst(rst),
      .is_random_rsc_dat(is_random_rsc_dat),
      .valid_rsc_dat(valid_rsc_dat),
      .epsilon_rsc_dat(epsilon_rsc_dat)
    );
endmodule
