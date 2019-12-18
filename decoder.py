#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 14:18:49 2019

@author: gal3li0
"""
#
#            I_clk : in  STD_LOGIC;
#           I_dataInst : in  STD_LOGIC_VECTOR (15 downto 0);
#           I_en : in  STD_LOGIC;
#           O_selA : out  STD_LOGIC_VECTOR (2 downto 0);
#           O_selB : out  STD_LOGIC_VECTOR (2 downto 0);
#           O_selD : out  STD_LOGIC_VECTOR (2 downto 0);
#           O_dataIMM : out  STD_LOGIC_VECTOR (15 downto 0);
#           O_regDwe : out  STD_LOGIC;
#           O_aluop : out  STD_LOGIC_VECTOR (4 downto 0));



from migen import *
from migen.genlib.fsm import *
from migen.fhdl import verilog
from migen.build.generic_platform import *
import math
import random


class Decoder(Module):
    def __init__(self):
        
        ###Input
        self.I_clk = I_clk = Signal()
        self.I_dataInst = I_dataInst = Signal(16)
        self.I_en = I_en = Signal()
        
        
        ###Output
        self.O_selA = O_selA = Signal(3)
        self.O_selB = O_selB = Signal(3)
        self.O_selD = O_selD = Signal(3)
        self.O_dataIMM = O_dataIMM = Signal(16)
        self.O_regDwe = O_regDwe = Signal()
        self.O_aluop = O_aluop = Signal(5)
        
        
        self.sync += \
            If(I_en,
               O_selD.eq(self.I_dataInst[9:12]),
               O_selA.eq(self.I_dataInst[5:8]),
               O_selB.eq(self.I_dataInst[2:5]),
               O_dataIMM.eq(Cat(self.I_dataInst[0:8], self.I_dataInst[0:8])),
               O_aluop.eq(Cat(self.I_dataInst[8], self.I_dataInst[12:16])),
               
               Case(self.I_dataInst[12:16], {
                            0b0111: O_regDwe.eq(0),
                            0b1100: O_regDwe.eq(0),
                            0b1101: O_regDwe.eq(0),
                            "default": O_regDwe.eq(1)
                            })
               )
            
            
               
def decoder_test(dut):
    #Test writing to registers and write read at the same time.
    yield dut.I_en.eq(1)
    for i in range(6):
        yield dut.I_dataInst.eq(random.randint(30000,40012))
        yield
        #test WE pin


               
               
if __name__ == "__main__":
    dut= Decoder()
    print(verilog.convert(Decoder()))
    run_simulation(dut, decoder_test(dut), vcd_name="decoder_test.vcd")