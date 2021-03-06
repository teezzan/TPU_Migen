#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 02:23:27 2019

@author: gal3li0
"""
from migen import *
from migen.fhdl import verilog

class Control_Unit(Module):
    def __init__(self):
        self.I_clk = I_clk = Signal()
        self.I_reset = I_reset = Signal()
        self.O_state = O_state = Signal(6, reset=0b000001)
        self.dum = dum = Signal()
        s_state = Signal(6, reset=0b000001)
         
        self.comb += dum.eq(O_state[3])
        self.sync += \
        [If(I_reset,
                    O_state.eq(0b000001)     ),
        
            Case(O_state, {
                                0b000001: O_state.eq(0b000010),
                                0b000010: O_state.eq(0b000100),
                                0b000100: O_state.eq(0b001000),
                                0b001000: O_state.eq(0b010000),
                                0b010000: O_state.eq(0b000001),
                                "default": O_state.eq(0b000001)
                                }),
#            O_state.eq(s_state)
                   ]
    
#print(verilog.convert(Control_Unit()))
def cpu_test(dut):
    #Test writing to registers and write read at the same time.
    
    yield dut.I_reset.eq(1)
    yield
    yield dut.I_reset.eq(0)
    yield
    yield
    yield
    yield
    yield
    yield
    yield
    yield
    yield
    yield
    yield
    yield
    yield
    
    
    while dut.dum: 
        yield
    yield
#    while dut.O_state[3] == 0: 
#        yield
#    yield
#    while dut.O_state[3] == 0: 
#        yield
    
        #test WE pin


if __name__ == "__main__":
    dut= Control_Unit()
    run_simulation(dut, cpu_test(dut), vcd_name="cntrol_unit.vcd")