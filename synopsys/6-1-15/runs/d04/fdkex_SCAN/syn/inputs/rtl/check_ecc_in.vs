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
/// check_ecc_in.vs
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
/// This block implements the Check ECC for ALU input data.
/// It corrects single error and detects double errors.
///
///=====================================================================================================================

///=====================================================================================================================
///                              check_ecc_in Module Instantiation
///=====================================================================================================================

module check_ecc_in (rstb, clk, mask, data_ecc, data_rxc, flag_ded);

///=====================================================================================================================
///                              Global Parameters and Functions
///=====================================================================================================================

	`include "parameters.vs"		
	`include "functions.vs"
	
///=====================================================================================================================
///                              check_ecc_in IO Declarations
///=====================================================================================================================

	input  rstb;
	input  clk;
	input  [width_data-1:0] mask [0:width_sec-1];
	input  [width_data_ecc-1:0] data_ecc;
	output logic [width_data-1:0] data_rxc;
	output logic flag_ded;

///=====================================================================================================================
///                              check_ecc_in Internal Signal Declarations
///=====================================================================================================================

	logic [width_ecc-1:0] ecc_rx;	
	
///=====================================================================================================================
///                              Main check_ecc_in Logic
///=====================================================================================================================

///=====================================================================================================================
///                              Received data ECC Generation
///=====================================================================================================================

	gen_ecc_in	gen_ecc_in0	(rstb, clk, data_ecc[width_data-1:0], mask, ecc_rx);

///=====================================================================================================================
///                              SECDED on Received data
///=====================================================================================================================

	secded_in	secded_in0	(rstb, clk, data_ecc[width_data_ecc-1:width_data_ecc-width_ecc], ecc_rx, data_ecc[width_data-1:0], data_rxc, flag_ded);
	
endmodule	// module check_ecc_in
