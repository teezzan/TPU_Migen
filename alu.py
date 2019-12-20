#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 18:10:03 2019

@author: gal3li0
"""


#    I_clk : in  STD_LOGIC;
#    I_en :  in  STD_LOGIC;
#    I_dataA :   in STD_LOGIC_VECTOR (15 downto 0);
#    I_dataB :   in STD_LOGIC_VECTOR (15 downto 0);
#    I_dataDwe : in STD_LOGIC;
#    I_aluop :   in STD_LOGIC_VECTOR (4 downto 0);
#    I_PC :      in STD_LOGIC_VECTOR (15 downto 0);
#    I_dataIMM : in STD_LOGIC_VECTOR (15 downto 0);
#    O_dataResult :   out  STD_LOGIC_VECTOR (15 downto 0);
#    O_dataWriteReg : out STD_LOGIC;
#    O_shouldBranch : out std_logic
    
    
from migen import *
from migen.genlib.fsm import *
from migen.fhdl import verilog
from migen.build.generic_platform import *
import math
import random
#
#-- cmp output bits
CMP_BIT_EQ= 14;
CMP_BIT_AGB= 13;
CMP_BIT_ALB= 12;
CMP_BIT_AZ= 11;
CMP_BIT_BZ= 10;


CJF_EQ = 0b000
CJF_AZ = 0b001
CJF_BZ = 0b010
CJF_ANZ = 0b011
CJF_BNZ = 0b100
CJF_AGB = 0b101
CJF_ALB = 0b110

OPCODE_ADD = 0b0000
OPCODE_SUB =  0b0001
OPCODE_OR = 0b0010
OPCODE_XOR =  0b0011
OPCODE_AND =  0b0100
OPCODE_NOT =  0b0101
OPCODE_READ =  0b0110
OPCODE_WRITE =  0b0111
OPCODE_LOAD =  0b1000
OPCODE_CMP =  0b1001
OPCODE_SHL =  0b1010
OPCODE_SHR =  0b1011
OPCODE_JUMP =  0b1100
OPCODE_JUMPEQ =  0b1101
OPCODE_SPEC =  0b1110
OPCODE_RES2 =  0b1111


class Alu(Module):
    def __init__(self):
        self.I_clk = I_clk = Signal()
        self.I_en = I_en = Signal()
        self.I_dataA = I_dataA = Signal(16)
        self.I_dataB = I_dataB = Signal(16)
        self.I_dataDwe = I_dataDwe = Signal()
        self.I_aluop = I_aluop = Signal(5)
        self.I_PC = I_PC = Signal(16)
        self.I_dataIMM = I_dataIMM = Signal(16)

        ###Output
        self.O_dataResult = O_dataResult = Signal(16)
        self.O_dataWriteReg = O_dataWriteReg = Signal()
        self.O_shouldBranch = O_shouldBranch = Signal()
        self.a_sign = a_sign = Signal((17,1))
        self.b_sign = b_sign = Signal((17,1))
        ###
        self.s_result = s_result = Signal(18)
        self.s_shouldBranch = s_shouldBranch = Signal()
        
        self.I_idata = I_idata =Signal(16)
        self.O_memMode = O_memMode = Signal()
#            I_set_idata:in STD_LOGIC;                  -- set interrup register data
#            I_set_irpc: in STD_LOGIC;                  -- set interrupt return pc
#            O_int_enabled: out STD_LOGIC;
            
        
        self.comb += [
            If(I_en,
                  O_dataWriteReg.eq(I_dataDwe),
#                  Display("Count"),
                   
                   Case(self.I_aluop[1:5], {
                                OPCODE_ADD: [If(I_aluop[0] == 0, 
                                            If(I_dataIMM[0] == 0,
                                                    s_result[0:17].eq(Cat(I_dataA,0b0) + Cat(I_dataB,0b0))
                                                    ).Else(s_result[0:17].eq(Cat(I_dataA,0b0) + I_dataIMM[1:5]))
                                        
                                        ).Else(a_sign.eq(Cat(I_dataA,I_dataA[15])),
                                                  b_sign.eq(Cat(I_dataB,I_dataB[15])),
                                                  s_result[0:17].eq(a_sign + b_sign)
                                                ),
                                            s_shouldBranch.eq(0)
                                        ],
    
    
                                    OPCODE_SUB: [If(I_aluop[0] == 0, 
                                            If(I_dataIMM[0] == 0,
                                                    s_result[0:17].eq(Cat(I_dataA,0b0) - Cat(I_dataB,0b0))
                                                    ).Else(s_result[0:17].eq(Cat(I_dataA,0b0) - I_dataIMM[1:5]))
                                        
                                        ).Else(a_sign.eq(Cat(I_dataA,I_dataA[15])),
                                                  b_sign.eq(Cat(I_dataB,I_dataB[15])),
                                                  s_result[0:17].eq(a_sign - b_sign)
                                                ),
                                            s_shouldBranch.eq(0)
                                        ],
                                
                                
                                
                                OPCODE_OR: [s_result[0:16].eq(I_dataA | I_dataB),
                                         s_shouldBranch.eq(0)
                                         ],
                                
                                OPCODE_XOR: [s_result[0:16].eq(I_dataA ^ I_dataB),
                                         s_shouldBranch.eq(0)
                                         ],
                                OPCODE_AND: [s_result[0:16].eq(I_dataA & I_dataB),
                                         s_shouldBranch.eq(0)
                                         ],
                                OPCODE_NOT: [s_result[0:16].eq(~I_dataA),
                                         s_shouldBranch.eq(0)
                                         ],
                                
                                OPCODE_READ: [a_sign.eq(I_dataA),
                                         b_sign.eq(I_dataB[0:5]),
                                         s_result[0:16].eq(a_sign + b_sign),                                  
                                         s_shouldBranch.eq(0),
                                         O_memMode.eq(I_aluop[0])
                                         ],
                        #write        
                                OPCODE_WRITE: [a_sign.eq(I_dataA),
                                         b_sign.eq(I_dataB[11:16]),
                                         s_result[0:16].eq(a_sign + b_sign),                                  
                                         s_shouldBranch.eq(0),
                                         O_memMode.eq(I_aluop[0])
                                         ],
                                
                                OPCODE_LOAD: [a_sign.eq(I_dataA),
                                         b_sign.eq(I_dataB[11:16]),
                                         s_result[0:16].eq(a_sign + b_sign),                                  
                                         s_shouldBranch.eq(0),
                                         O_memMode.eq(I_aluop[0])
                                         ],
#                                
                                
                                OPCODE_CMP: [
                                        Display("Count"),
                                        If(I_dataA == I_dataB, 
                                            s_result[CMP_BIT_EQ].eq(1)
                                        ).Else(s_result[CMP_BIT_EQ].eq(0)
                                                ),
                                
                                        If(I_dataA == 0, 
                                            s_result[CMP_BIT_AZ].eq(1)
                                        ).Else(s_result[CMP_BIT_AZ].eq(0)
                                                ),
                                        
                                        If(I_dataB == 0, 
                                            s_result[CMP_BIT_BZ].eq(1)
                                        ).Else(s_result[CMP_BIT_BZ].eq(0)
                                                ),
                                        
                                        If(I_aluop[0] == 0, 
                                           If(I_dataA > I_dataB,
                                               s_result[CMP_BIT_AGB].eq(1)
                                                   ).Else( s_result[CMP_BIT_AGB].eq(0)),
                                           
                                           If(I_dataA < I_dataB,
                                               s_result[CMP_BIT_ALB].eq(1)
                                                   ).Else( s_result[CMP_BIT_ALB].eq(0))
                                           
                                        ).Else(a_sign.eq(I_dataA),
                                              b_sign.eq(I_dataB),
                                              
                                              If(a_sign > b_sign,
                                               s_result[CMP_BIT_AGB].eq(1)
                                                   ).Else( s_result[CMP_BIT_AGB].eq(0)),
                                           
                                           If(a_sign < b_sign,
                                               s_result[CMP_BIT_ALB].eq(1)
                                                   ).Else( s_result[CMP_BIT_ALB].eq(0))
                                                
                                                ),
                                           s_result[15].eq(0),
                                           s_result[0:10].eq(0b0000000000),
                                           s_shouldBranch.eq(0)    
                                        ],
                                #Lshift
                                
                                OPCODE_SHL: [
                                        Case(self.I_dataB[0:4], {
                                                1: s_result[0:16].eq(I_dataA << 1),
                                                2: s_result[0:16].eq(I_dataA << 2),
                                                3: s_result[0:16].eq(I_dataA << 3),
                                                4: s_result[0:16].eq(I_dataA << 4),
                                                5: s_result[0:16].eq(I_dataA << 5),
                                                6: s_result[0:16].eq(I_dataA << 6),
                                                7: s_result[0:16].eq(I_dataA << 7),
                                                8: s_result[0:16].eq(I_dataA << 8),
                                                9: s_result[0:16].eq(I_dataA << 9),
                                                10: s_result[0:16].eq(I_dataA << 10),
                                                11: s_result[0:16].eq(I_dataA << 11),
                                                12: s_result[0:16].eq(I_dataA << 12),
                                                13: s_result[0:16].eq(I_dataA << 13),
                                                14: s_result[0:16].eq(I_dataA << 14),
                                                15: s_result[0:16].eq(I_dataA << 15),
                                                "default": s_result[0:16].eq(I_dataA)
                                            }),
                                            s_shouldBranch.eq(0)
                                        ],
                                
                                #Rshift
                                
                                OPCODE_SHR: [
                                        Case(self.I_dataB[0:4], {
                                                1: s_result[0:16].eq(I_dataA >> 1),
                                                2: s_result[0:16].eq(I_dataA >> 2),
                                                3: s_result[0:16].eq(I_dataA >> 3),
                                                4: s_result[0:16].eq(I_dataA >> 4),
                                                5: s_result[0:16].eq(I_dataA >> 5),
                                                6: s_result[0:16].eq(I_dataA >> 6),
                                                7: s_result[0:16].eq(I_dataA >> 7),
                                                8: s_result[0:16].eq(I_dataA >> 8),
                                                9: s_result[0:16].eq(I_dataA >> 9),
                                                10: s_result[0:16].eq(I_dataA >> 10),
                                                11: s_result[0:16].eq(I_dataA >> 11),
                                                12: s_result[0:16].eq(I_dataA >> 12),
                                                13: s_result[0:16].eq(I_dataA >> 13),
                                                14: s_result[0:16].eq(I_dataA >> 14),
                                                15: s_result[0:16].eq(I_dataA >> 15),
                                                "default": s_result[0:16].eq(I_dataA)
                                            }),
                                            s_shouldBranch.eq(0)
                                        ],
                                
                                OPCODE_JUMP: [If(I_aluop[0] == 0, 
                                            s_result[0:16].eq(I_dataA)
                                        ).Else(
                                              a_sign.eq(I_PC),
                                              b_sign.eq(Cat(0b0,I_dataIMM[0:11])),                                                
                                              s_result[0:16].eq(a_sign + b_sign)
                                                ),
                                            s_shouldBranch.eq(1)
                                        ],
                                
                                OPCODE_JUMPEQ: [If(I_aluop[0] == 1, 
                                            a_sign.eq(I_PC),
                                            b_sign.eq(I_dataIMM[0:5]),                                                
                                            s_result[0:16].eq(a_sign + b_sign)
                                            
                                        ).Else(
                                              s_result[0:16].eq(I_dataB)
                                                ),
                                
                                            Case(self.I_dataIMM[13:16], {
                                                CJF_EQ: s_shouldBranch.eq(CMP_BIT_EQ),
                                                CJF_AZ: s_shouldBranch.eq(CMP_BIT_AZ),
                                                CJF_BZ: s_shouldBranch.eq(CMP_BIT_BZ),
                                                CJF_ANZ: s_shouldBranch.eq(CMP_BIT_AZ),
                                                CJF_BNZ: s_shouldBranch.eq(CMP_BIT_BZ),
                                                CJF_AGB: s_shouldBranch.eq(CMP_BIT_AGB),
                                                CJF_ALB: s_shouldBranch.eq(CMP_BIT_ALB),
                                                "default": s_shouldBranch.eq(0)
                                                })
                                            
                                        ],
                                
#                                0b1101: O_regDwe.eq(0),
                                "default": b_sign.eq(1)
                                })
                   )]
    
        self.comb += [
                O_dataResult.eq(s_result[0:16]),
                O_shouldBranch.eq(s_shouldBranch)]
#        
#I_dataA <= X"0001";
#I_dataB <= X"0002";
#I_aluop <= OPCODE_ADD & '0';
#I_dataIMM <= X"F1FA";
# 
#wait for I_clk_period;
#I_dataA <= X"0005";
#I_dataB <= X"0003";
#I_aluop <= OPCODE_SUB & '0';
# 
#wait for I_clk_period;
# 
#I_dataA <= X"FEEE";
#I_dataB <= X"0000";
#I_aluop <= OPCODE_CMP & '0';
        
def ALU_test(dut):
    #Test writing to registers and write read at the same time.
    yield dut.I_en.eq(1)
    
    yield dut.I_dataA.eq(0x0001)
    yield dut.I_dataB.eq(0x0002)
    yield dut.I_aluop.eq(0b00000)
    yield dut.I_dataIMM.eq(0xF1FA)
    yield
    
    yield dut.I_dataA.eq(0x0005)
    yield dut.I_dataB.eq(0x0003)
    yield dut.I_aluop.eq(0b00010)
    yield
    
    yield dut.I_dataA.eq(0xfeee)
    yield dut.I_dataB.eq(0x0000)
    yield dut.I_aluop.eq(0b10010)
    yield
    
    yield dut.I_dataA.eq(0xabcd)
    yield dut.I_dataB.eq(0xabcd)
    yield dut.I_aluop.eq(0b10010)
    yield
    
    yield dut.I_dataA.eq(0x0001)
    yield dut.I_dataB.eq(0x0002)
    yield dut.I_aluop.eq(0b00000)
    yield dut.I_dataIMM.eq(0xF1FA)
    yield
    
    yield dut.I_dataA.eq(0x0051)
    yield dut.I_dataB.eq(0x0562)
    yield dut.I_aluop.eq(0b00000)
    yield dut.I_dataIMM.eq(0xF1FA)
    yield
    
    yield dut.I_dataA.eq(0xfeee)
    yield dut.I_dataB.eq(0x0000)
    yield dut.I_aluop.eq(0b10010)
    yield
    
    yield dut.I_dataA.eq(0xabdd)
    yield dut.I_dataB.eq(0xabdd)
    yield dut.I_aluop.eq(0b10010)
    yield
    
if __name__ == "__main__":
    dut= Alu()
#    print(verilog.convert(Decoder()))
    run_simulation(dut, ALU_test(dut), vcd_name="ALU_test.vcd")        
#    print(verilog.convert(Alu()))       