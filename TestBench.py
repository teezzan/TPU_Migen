#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 09:48:11 2019

@author: gal3li0
"""

from migen import *
from migen.genlib.fsm import *
from migen.fhdl import verilog
from migen.build.generic_platform import *
from reg_file import Register_File
from decoder import Decoder
from alu import Alu
from control_unit import Control_Unit
import random

class cpu(Module):
    def __init__(self):
        
        ###Input
        self.I_clk = I_clk = Signal()     
        self.instruction = instruction = Signal(16) 
        self.instructions = instructions = Array(Signal(16) for a in range(4))
        
        
        self.en = en = Signal()
        self.dataA = dataA = Signal(16)
        self.dataB = dataB = Signal(16)
        self.selA = selA = Signal(3)
        self.selB = selB = Signal(3)
        self.selD = selD = Signal(3)
        
        self.dataIMM = dataIMM = Signal(16)
        self.dataDwe = dataDwe = Signal()
        self.aluop = aluop = Signal(5)
        self.PC = PC = Signal(16)
        
        self.dataResult = dataResult = Signal(16)
        self.dataWriteReg = dataWriteReg = Signal()
        self.shouldBranch = shouldBranch = Signal()
        
        self.en_regread = en_regread = Signal()
        self.en_regwrite = en_regwrite = Signal()
        self.en_decode = en_decode = Signal()
        self.en_alu = en_alu = Signal()
        
        self.reset = reset = Signal()
        i = Signal(2)
        
        alu=Alu()
        self.submodules += alu
        
        decoder=Decoder()
        self.submodules += decoder
        
        reg=Register_File()
        self.submodules += reg
        
        control=Control_Unit()
        self.submodules += control
        
        self.sync +=[
                If(en_regwrite,
                   i.eq(i+1),
                   instruction.eq(instructions[i])
                   )
                ]
        
        self.comb += [
                instructions[0].eq(0x8902),
        instructions[1].eq(0x0670),
        instructions[2].eq(0x2a0c),
        instructions[3].eq(0x2a0c),
                
            control.I_reset.eq(reset),
            en_regwrite.eq(control.O_state[3]),
            en_regread.eq(control.O_state[1]),
            en_alu.eq(control.O_state[2]),
            en_decode.eq(control.O_state[0]),
                
                
            en.eq(1),
            alu.I_clk.eq(I_clk),
#            alu.I_en.eq(en_alu),
            alu.I_en.eq(1),
            alu.I_dataA.eq(dataA),
            alu.I_dataB.eq(dataB),
            alu.I_dataDwe.eq(dataDwe),
            alu.I_aluop.eq(aluop),
            alu.I_PC.eq(PC),
            alu.I_dataIMM.eq(dataIMM),
            dataResult.eq(alu.O_dataResult),
            dataWriteReg.eq(alu.O_dataWriteReg),
            shouldBranch.eq(alu.O_shouldBranch),
            
            decoder.I_en.eq(en_decode),
            selA.eq(decoder.O_selA),
            selB.eq(decoder.O_selB),
            selD.eq(decoder.O_selD),
            dataIMM.eq(decoder.O_dataIMM),
            dataDwe.eq(decoder.O_regDwe),
            aluop.eq(decoder.O_aluop),
            decoder.I_dataInst.eq(instruction),
            decoder.I_clk.eq(I_clk),
            decoder.I_en.eq(en),
            
            reg.I_clk.eq(I_clk),
            reg.I_en.eq(en_regread | en_regwrite),
            reg.I_dataD.eq(dataResult),
            reg.I_selA.eq(selA),
            reg.I_selB.eq(selB),
            reg.I_selD.eq(selD),
            reg.I_we.eq(dataWriteReg & en_regwrite),
            dataA.eq(reg.O_dataA),
            dataB.eq(reg.O_dataB)
              
        
        ]
        
        
        
def cpu_test(dut):
    #Test writing to registers and write read at the same time.
    yield dut.en.eq(1)
    yield dut.reset.eq(1)
    yield
    yield
    yield dut.reset.eq(0)
    yield
#    yield
#    yield
#    yield
#    yield
#    yield
#    yield
#    yield
#    yield
#    yield
#    yield
#    yield
#    yield
#    yield
#    yield
#    yield
#    yield
#    yield
#    yield
#    yield
    for i in range(100):
        yield
##    yield dut.instruction.eq(0x8701)    
#    while dut.en_regwrite == 0: 
#        yield
#    yield dut.instruction.eq(0x8902)
#    yield
#    while dut.en_regwrite == 0: 
#        yield
#    yield dut.instruction.eq(0x0670) #0x2a0c
#    yield
#    while dut.en_regwrite == 0: 
#         yield
#        
#    yield dut.instruction.eq(0x2a0c)
#    yield
#    while dut.en_regwrite == 0: 
#        yield
#    
        #test WE pin


if __name__ == "__main__":
    dut= cpu()
    run_simulation(dut, cpu_test(dut), vcd_name="cpu_test.vcd")
#    print(verilog.convert(cpu()))