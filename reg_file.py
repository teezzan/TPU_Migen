#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 11:45:50 2019

@author: gal3li0
"""
    
from migen import *
from migen.genlib.fsm import *
from migen.fhdl import verilog
from migen.build.generic_platform import *
import math
import random

class Register_File(Module):
    def __init__(self):
        ###Input
        self.I_clk = I_clk = Signal()
        self.I_en = I_en = Signal()
        self.I_dataD = I_dataD = Signal(16)
        self.I_selA = I_selA = Signal(3)
        self.I_selB = I_selB = Signal(3)
        self.I_selD = I_selD = Signal(3)
        self.I_we = I_we = Signal()
        
        ###Output
        self.O_dataA = O_dataA = Signal(16)
        self.O_dataB = O_dataB = Signal(16)
        
        ###registers
        self.regs = regs = Array(Signal(16) for a in range(8))
        
        
        self.sync += \
            If(I_en,
               O_dataA.eq(regs[I_selA]),
               O_dataB.eq(regs[I_selB]),
               If(I_we,
                  regs[I_selD].eq(I_dataD)
                  )
               )
               
def Reg_test(dut):
    #Test writing to registers and write read at the same time.
    yield dut.I_en.eq(1)
    yield dut.I_we.eq(1)
    for i in range(16):
        yield dut.I_dataD.eq(random.randint(0,16))
        yield dut.I_selD.eq(2*i)
        yield
        #test WE pin
    yield dut.I_we.eq(0)
    for i in range(16):
        yield dut.I_dataD.eq(random.randint(0,16))
        yield dut.I_selD.eq(5*i)
        yield
        # Test read
    yield dut.I_we.eq(0)
    for i in range(16):
        yield dut.I_selA.eq(i)
        yield dut.I_selB.eq(16-i)
        yield

               
               
if __name__ == "__main__":
    dut= Register_File()
    run_simulation(dut, Reg_test(dut), vcd_name="RegFile_test.vcd")