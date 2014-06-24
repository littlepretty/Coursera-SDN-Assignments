
--
--  https://github.storm.gatech.edu/NetASM
--
--  File:
--        ACL/Code.hs
--
--  Project:
--        NetASM: A Network Assembly for Orchestrating Programmable Network Devices
--
--  Author:
--        Muhammad Shahbaz
--
--  Copyright notice:
--        Copyright (C) 2014 Georgia Institute of Technology
--           Network Operations and Internet Security Lab
--
--  Licence:
--        This file is a part of the NetASM development base package.
--
--        This file is free code: you can redistribute it and/or modify it under
--        the terms of the GNU Lesser General Public License version 2.1 as
--        published by the Free Software Foundation.
--
--        This package is distributed in the hope that it will be useful, but
--        WITHOUT ANY WARRANTY; without even the implied warranty of
--        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
--        Lesser General Public License for more details.
--
--        You should have received a copy of the GNU Lesser General Public
--        License along with the NetASM source package.  If not, see
--        http://www.gnu.org/licenses/.

{-
  Coursera:
    Software Defined Networking (SDN) course
    Module X Programming Assignment
  
  Professor: Nick Feamster
  Developer: Muhammad Shahbaz
-}

module Apps.ACL_Assignment_YJQ.Code where

import Utils.Map
import Core.Language
import Core.PacketParser

----------------------------------------------------------
-- Access Control List (ACLs with Simple MAC Learning) ---
----------------------------------------------------------

-- Table size
tbl_size = 10

-- Match table specs with default values
mtch_size = tbl_size                                        -- table size
mtch_tbl  = Dynamic("mtch0", (mtch_size, ["dstmac"]))       -- dynamic table "mtch0"
mtch_val  = Static([[("dstmac", 0)] | x <- [1..mtch_size]]) -- default values
mtch_ptrn = [("dstmac", "srcmac")]                          -- pattern for loading the match table

-- Modify table specs with default values
mdfy_size = tbl_size                                         -- table size
mdfy_tbl  = Dynamic("mdfy0", (mdfy_size, ["outport"]))       -- dynamic table "mdfy0"
mdfy_val  = Static([[("outport", 0)] | x <- [1..mdfy_size]]) -- default values      
mdfy_ptrn = [("outport", "inport")]                          -- pattern for loading the modify table

{- 
  TODO: Specify a dynamic table for implementing access control.
        The table should have the following specs:
          1. Two columns for holding source and destination MAC pair i.e., "srcmac" and "dstmac"
          2. A table size of 5
          3. Default values of zero (0)
        (Hint: see how the match/modify tables have been defined above)
-}
acl_size = 5
acl_tbl = Dynamic("acl0", (acl_size, ["srcmac", "dstmac"]))
acl_val = Static([[("srcmac", 0), ("dstmac", 0)] | x <- [1..acl_size]])
--act_ptrn = [("srcmac", "srcmac"), ("dstmac", "dstmac")]



-- Initialisation code for MAC learning with access control
ic = [MKT(mtch_tbl, mtch_val) -- create match table with given table type and default values
    , MKT(mdfy_tbl, mdfy_val) -- create modify table with given table type and default values
    , MKR("r", 0)             -- create register 'r' to index currently selected row in match/modify tables
{-
  TODO: Create the ACL table with the defined specs using the MKT instruction.
        (Hint: see how the match/modify tables are created in the instructions, above)
-}
    , MKT(acl_tbl, acl_val)

    ]                                  

-- Topology code for MAC learning with access control
tc = [
    -- MAC Learning
      IBRTF(mtch_tbl, "i", "lbl_miss")         -- if (match on mtch_tbl) then set index field "i" in the header with matched index and goto next instruction else jump to label "lbl_miss"
    , LDFTF(mdfy_tbl, "i")                     -- load header with md_t table content at index "i"
    , JMP("lbl_acl")                           -- jump to label "lbl_acl" i.e., perform access control
    , LBL("lbl_miss")                          -- label "l_miss"
    , LDTFR(mtch_tbl, mtch_ptrn, "r")          -- update "dstmac" in the mtch_tbl at location "r" with "srcmac" from the header
    , LDTFR(mdfy_tbl, mdfy_ptrn, "r")          -- update "outport" in the mdfy_tbl at location "r" with "inport" from the header
    , OPF("outport", "inport", Xor, _1s)       -- set "outport" (bitmap) to all 1s except for the "inport" i.e., flood the packet
    , OPR("r", "r", Add, 1)                    -- increment register "r" i.e., move the current index to next row
    , BRR("r", Lt, tbl_size, "lbl_acl")        -- if (register "r" less than tbl_size) then jump to label "lbl_acl" else goto next instruction
    , LDR("r", 0)                              -- set register "r" to 0 
    , LBL("lbl_acl")                           -- label "lbl_acl"  
    
{- Access Control
  TODO: Add assembly code for implementing access control using BRTF and DRP.
        1. Use the BRTF instruction to compare the header with the ACL table
        2. Use the DRP instruction to tag the header as dropped
-}
    , BRTF(acl_tbl, "i", "lbl_drop")
    , JMP("lbl_end")
    , LBL("lbl_drop")
    , DRP
    , LBL("lbl_end")                           -- label "lbl_end"
    , HLT]                                     -- halt
