#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 15:12:13 2019

@author: gal3li0
"""

from migen import *
from migen.fhdl import verilog
from migen.build.generic_platform import *
import math
import random


class Pc_unit(Module):
    def __init__(self):
        
        ###Input
        self.I_clk = I_clk = Signal()
        self.I_nPC = I_nPC = Signal(16)
        self.I_nPCop = I_nPCop = Signal(2)
        self.I_intVec = I_intVec = Signal()
        
        ###signal
        self.current_pc = current_pc = Signal(16, reset=0)
        ###Output
        self.O_PC = O_PC = Signal(16)
#        0008
        self.sync += \
        [     Case(I_nPCop, {
                                0b00: [If(I_intVec == 1,
                                          current_pc.eq(0x0008)
                                          )] ,
                                0b01: current_pc.eq(current_pc + 1),
                                0b10: current_pc.eq(I_nPC),
                                0b11: current_pc.eq(0x0000),
                                "default": []
                                }),
            O_PC.eq(current_pc)
                   ]
def pc_test(dut):
    #Test writing to registers and write read at the same time.
    for i in range(16):
        yield dut.I_nPC.eq(random.randint(30000,40012))
        yield dut.I_nPCop.eq(0b01)
        yield
        #test WE pin


               
               
if __name__ == "__main__":
    dut= Pc_unit()
#    print(verilog.convert(Decoder()))
    run_simulation(dut, pc_test(dut), vcd_name="pc_test.vcd")