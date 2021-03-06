/* 
**************************************************************************
 * Intel Top Secret
 ****************************************************************************
 * Copyright (C) 2012, Intel Corporation.  All rights reserved.
 *
 * This is the property of Intel Corporation and may only be utilized
 * pursuant to a written Restricted Use Nondisclosure Agreement
 * with Intel Corporation.  It may not be used, reproduced, or
 * disclosed to others except in accordance with the terms and 
 * conditions of such agreement.
 ****************************************************************************
*/

///=====================================================================================================================
///
/// gen_ecc_alu.vs
///
/// Primary Contact   : 
/// Secondary Contact : 
/// Unit Owner        : 
///
/// Original Author   : Jina Kim
/// Original Date     : 14 September 2009
/// Last Modified     : 18 January 2010
///
/// Copyright (c) 2009 Intel Corporation
/// Intel Proprietary
///
/// This block implements the extended Hamming code generation for ALU output data.
/// It generates Hamming code and overall parity.
///
///=====================================================================================================================

///=====================================================================================================================
///                              gen_ecc_alu Module Instantiation
///=====================================================================================================================

module gen_ecc_alu (rstb, clk, din, mask, ecc);

///=====================================================================================================================
///                              Global Parameters and Functions
///=====================================================================================================================

	`include "parameters.vs"
	`include "functions.vs"	
	
///=====================================================================================================================
///                              gen_ecc_alu IO Declarations
///=====================================================================================================================

	input  rstb;
	input  clk;
	input  [width_data-1:0] din;
	input  [width_data-1:0] mask [0:width_sec-1];
	output logic [width_ecc-1:0] ecc;

///=====================================================================================================================
///                              Main gen_ecc_alu Logic
///=====================================================================================================================

///=====================================================================================================================
///                              Hamming Code and Parity Generation
///=====================================================================================================================

// ECC bits except the MSB: Hamming code
// MSB of ECC: Overall parity
	always_ff @ (negedge rstb, posedge clk) begin
		if (!rstb) begin
	  		ecc <= {width_ecc{1'b0}};
	  	end else begin	
			ecc[width_sec-1:0] <= {^(din&mask[7]), ^(din&mask[6]), ^(din&mask[5]), ^(din&mask[4]), ^(din&mask[3]), ^(din&mask[2]), ^(din&mask[1]), ^(din&mask[0])};
			ecc[width_ecc-1] <= ^{din, ecc[width_sec-1:0]};	// Append parity at MSB of Hamming code
		end
	end 
	
endmodule	// module gen_ecc_alu
