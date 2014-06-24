---------------------------------------------------------------------------------
--
--  https://github.storm.gatech.edu/NetASM
--
--  File:
--        ACL/Run.hs
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

module Apps.ACL_Assignment_YJQ.Run where

import Utils.Map
import Core.Language
import Core.PacketParser
import Apps.ACL_Assignment_YJQ.Code

----------------------------------------------------------
-- Access Control List (ACLs with Simple MAC Learning) ---
----------------------------------------------------------

-- Test header (a.k.a. packet) stream (only the required fields are listed in the header)
h0 = genHdr([("inport",     1)
            ,("outport",    0)
            ,("srcmac",     1234)
            ,("dstmac",     4321)
            ,("i",          0)])

h1 = genHdr([("inport",     3)
            ,("outport",    0)
            ,("srcmac",     6543)
            ,("dstmac",     5432)
            ,("i",          0)])

h2 = genHdr([("inport",     4)
            ,("outport",    0)
            ,("srcmac",     4321)
            ,("dstmac",     1234)
            ,("i",          0)])

h3 = genHdr([("inport",     2)
            ,("outport",    0)
            ,("srcmac",     5432)
            ,("dstmac",     6543)
            ,("i",          0)])

{- Test control stream
  TODO: Write rules in the ACL table using the WRT instruction.
        Create WRT instructions for the following rules:
          1. Write "srcmac"=6543 and "dstmac"=5432 at index 0
          2. Write "srcmac"=4321 and "dstmac"=1234 at index 1
        (Hint: look at the Apps/Passthrough/Run.hs file on how to use the WRT instruction)
-}
c0 = WRT(acl_tbl, [("srcmac", 6543), ("dstmac", 5432)], 0)
c1 = WRT(acl_tbl, [("srcmac", 4321), ("dstmac", 1234)], 1)



-- Input sequence
is = [
{- Test control stream
  TODO: Uncomment line 90 and 91 by removing --
-}
      CTRL(c0)
    , CTRL(c1)
    , HDR(h0) 
    , HDR(h1) 
    , HDR(h2) 
    , HDR(h3)]

-- Emulate the code
emulateEx :: [Hdr]
emulateEx = emulate(ic, is, tc)

-- Profile the code
profileEx :: String 
profileEx = profile(ic, is, tc)

-- main
main = do 
        putStrLn $ prettyPrint $ emulateEx
        putStrLn                 profileEx