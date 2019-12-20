#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 19:04:17 2019

@author: gal3li0
"""
from migen import *
from migen.genlib.fsm import *
from migen.fhdl import verilog
from migen.build.generic_platform import *
import math
import random


class Ram1(Module):
    def __init__(self):
        
        ###Input
        self.I_clk = I_clk = Signal()
        self.I_we = I_we = Signal()
        self.I_addr = I_addr = Signal(16)
        self.I_data = I_data = Signal(16)
        ###output
        self.O_data = O_data = Signal(16)
        ###storage
        self.ram_16 = ram_16 = Array(Signal(16) for a in range(32))
        
        
        self.sync += \
               If(I_we,
                  ram_16[I_addr].eq(I_data)
                  ).Else(O_data.eq(ram_16[I_addr])
                          )
               
               
class Mem_Ram(Module):
    def __init__(self):
        # Initialize the beginning of the memory with integers
        # from 0 to 19.
        self.specials.mem = Memory(16, 32, init=list(range(20)))


class Ram2(Module):
    def __init__(self):
        
        ###Input
        self.I_clk = I_clk = Signal()
        self.I_we = I_we = Signal()
        self.I_addr = I_addr = Signal(16)
        self.I_data = I_data = Signal(16)
        ###output
        self.O_data = O_data = Signal(16)
        
        Ram=Mem_Ram()
        self.submodules += Ram
#        led = self.Ram.led     
        
        self.sync += \
               If(I_we,
                  Ram.mem[I_addr].eq(I_data)
                  ).Else(O_data.eq(Ram.mem[I_addr])
                          )               
               
               
def Ram_test(dut):
    #Test writing to registers and write read at the same time.
    yield dut.I_we.eq(1)
    for i in range(8):
        yield dut.I_data.eq(random.randint(0,100))
        yield dut.I_addr.eq(random.randint(0,32))
        yield
        #test WE pin
    yield dut.I_we.eq(0)
    for i in range(8):
        yield dut.I_data.eq(random.randint(-100,0))
        yield dut.I_addr.eq(random.randint(0,32))
        yield

        
        
if __name__ == "__main__":
    dut1= Ram1()
    dut2= Ram2()
    run_simulation(dut1, Ram_test(dut1), vcd_name="Ram1_test.vcd")
    run_simulation(dut2, Ram_test(dut2), vcd_name="Ram2_test.vcd")


