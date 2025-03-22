#
#  prjpeppercorn -- GateMate FPGAs Bitstream Documentation and Tools
#
#  Copyright (C) 2024  The Project Peppercorn Authors.
#
#  Permission to use, copy, modify, and/or distribute this software for any
#  purpose with or without fee is hereby granted, provided that the above
#  copyright notice and this permission notice appear in all copies.
#
#  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#  WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#  ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#  ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#  OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

from enum import Enum
from dataclasses import dataclass

PLL_X_POS = 33
PLL_Y_POS = 131
SERDES_X_POS = 1
SERDES_Y_POS = 121
CTRL_X_POS = -2
CTRL_Y_POS = -2

def max_row():
    return 131

def max_col():
    return 163

def num_rows():
    return max_row() + 3

def num_cols():
    return max_col() + 3

def is_sb(x,y):
    if (x>=-1 and x<=162 and y>=-1 and y<=130):
        return (x+1) % 2 == (y+1) % 2
    return False

def is_sb_big(x,y):
    if (x>=-1 and x<=162 and y>=-1 and y<=130):
        if (x+1) % 2 == 1 and (y+1) % 2 == 1:
            return False if (x+1) % 4 == (y+1) % 4 else True
        if (x+1) % 2 == 0 and (y+1) % 2 == 0:
            return False if (x+1) % 4 != (y+1) % 4 else True
    return False

def is_sb_sml(x,y):
    if (x>=-1 and x<=162 and y>=-1 and y<=130):
        if (x+1) % 2 == 1 and (y+1) % 2 == 1:
            return True if (x+1) % 4 == (y+1) % 4 else False
        if (x+1) % 2 == 0 and (y+1) % 2 == 0:
            return True if (x+1) % 4 != (y+1) % 4 else False
    return False

def get_sb_type(x,y):
    return "SB_BIG" if is_sb_big(x,y) else "SB_SML"

def is_cpe(x,y):
    return x>=1 and x<=160 and y>=1 and y<=128

def is_outmux(x,y):
    return is_cpe(x,y) and (x+1) % 2 == (y+1) % 2

def is_edge_left(x,y):
    return x==-2 and y>=1 and y<=128

def is_edge_right(x,y):
    return x==max_col() and y>=1 and y<=128

def is_edge_bottom(x,y):
    return y==-2 and x>=1 and x<=160

def is_edge_top(x,y):
    return y==max_row() and x>=28 and x<=160

def is_edge_io(x,y):
    if (y==-2 and x>=5 and x<=40): # IO Bank S3/WA
        return True
    if (y==-2 and x>=57 and x<=92):  # IO Bank S1/WB
        return True
    if (y==-2 and x>=101 and x<=136): # IO Bank S2/WC
        return True
    if (x==-2 and y>=25 and y<=60): # IO Bank W1/SA
        return True
    if (x==-2 and y>=69 and y<=104): # IO Bank W2/SB
        return True
    if (x==max_col() and y>=25 and y<=60): # IO Bank E1/NA
        return True
    if (x==max_col() and y>=69 and y<=104): # IO Bank E2/NB
        return True
    if (y==max_row() and x>=57 and x<=92): # IO Bank N1/EA
        return True
    if (y==max_row() and x>=101 and x<=136): # IO Bank N2/EB
        return True

def is_ram(x,y):
    return x in [33,65,97,129] and y in [1,17,33,49,65,81,97,113]

@dataclass
class IOName:
    bank : str
    port : str
    num  : int

def get_io_name(x,y):
    if (y==-2 and x>=5 and x<=40): # IO Bank S3/WA
        x-=5
        return IOName("S3", "A" if x % 4==0 else "B", x//4)
    if (y==-2 and x>=57 and x<=92):  # IO Bank S1/WB
        x-=57
        return IOName("S1", "A" if x % 4==0 else "B", x//4)
    if (y==-2 and x>=101 and x<=136): # IO Bank S2/WC
        x-=101
        return IOName("S2", "A" if x % 4==0 else "B", x//4)
    if (x==-2 and y>=25 and y<=60): # IO Bank W1/SA
        y-=25
        return IOName("W1", "A" if y % 4==0 else "B", y//4)
    if (x==-2 and y>=69 and y<=104): # IO Bank W2/SB
        y-=69
        return IOName("W2", "A" if y % 4==0 else "B", y//4)
    if (x==max_col() and y>=25 and y<=60): # IO Bank E1/NA
        y-=25
        return IOName("E1", "A" if y % 4==0 else "B", y//4)
    if (x==max_col() and y>=69 and y<=104): # IO Bank E2/NB
        y-=69
        return IOName("E2", "A" if y % 4==0 else "B", y//4)
    if (y==max_row() and x>=57 and x<=92): # IO Bank N1/EA
        x-=57
        return IOName("N1", "A" if x % 4==0 else "B", x//4)
    if (y==max_row() and x>=101 and x<=136): # IO Bank N2/EB
        x-=101
        return IOName("N2", "A" if x % 4==0 else "B", x//4)

def is_gpio(x,y):
    if is_edge_io(x,y):
        if (y==-2 or y==max_row()):
            return x % 2==1
        if (x==-2 or x==max_col()):
            return y % 2==1
    return False

def is_pll(x,y):
    return x==PLL_X_POS and y==PLL_Y_POS

def is_serdes(x,y):
    return x==SERDES_X_POS and y==SERDES_Y_POS

def is_cfg_ctrl(x,y):
    return x==CTRL_X_POS and y==CTRL_Y_POS

def base_loc(x,y):
    return (((x-1) & ~1) + 1, ((y-1) & ~1) + 1)

class PinType(Enum):
    INPUT = 0
    OUTPUT = 1
    INOUT = 2

@dataclass(eq=True, order=True)
class Primitive:
    name : str
    type : str
    z    : int

@dataclass(eq=True, order=True)
class Pin:
    name : str
    dir  : PinType
    wire_type : str
    use_alias_conn: bool = False

@dataclass(eq=True, order=True)
class Group:
    name : str
    type : str

@dataclass(eq=True, order=True)
class Endpoint:
    name : str
    type : str

@dataclass(eq=True, order=True)
class MUX:
    src : str
    dst : str
    name : str
    bits : int
    value : int
    invert: bool
    visible: bool
    config: bool

@dataclass
class Location:
    x : int
    y : int

@dataclass(eq=True, order=True)
class Connection:
    x : int
    y : int
    name : str

@dataclass(eq=True, order=True)
class TileInfo:
    die : int
    bit_x : int
    bit_y : int
    prim_index : int

PRIMITIVES_PINS = {
    "CPE_HALF_U": [
        Pin("RAM_I"  ,PinType.INPUT,  "CPE_WIRE_L", True),
        Pin("IN1"    ,PinType.INPUT,  "CPE_WIRE_L", True),
        Pin("IN2"    ,PinType.INPUT,  "CPE_WIRE_L", True),
        Pin("IN3"    ,PinType.INPUT,  "CPE_WIRE_L", True),
        Pin("IN4"    ,PinType.INPUT,  "CPE_WIRE_L", True),
        Pin("CLK"    ,PinType.INPUT,  "CPE_WIRE_L", True),
        Pin("EN"     ,PinType.INPUT,  "CPE_WIRE_L", True),
        Pin("SR"     ,PinType.INPUT,  "CPE_WIRE_L", True),
        Pin("OUT"    ,PinType.OUTPUT, "CPE_WIRE_B", True),
        Pin("RAM_O"  ,PinType.OUTPUT, "CPE_WIRE_B", True),
    ],

    "CPE_HALF_L": [
        Pin("RAM_I"  ,PinType.INPUT,  "CPE_WIRE_L", True),
        Pin("IN1"    ,PinType.INPUT,  "CPE_WIRE_L", True),
        Pin("IN2"    ,PinType.INPUT,  "CPE_WIRE_L", True),
        Pin("IN3"    ,PinType.INPUT,  "CPE_WIRE_L", True),
        Pin("IN4"    ,PinType.INPUT,  "CPE_WIRE_L", True),
        Pin("CLK"    ,PinType.INPUT,  "CPE_WIRE_L", True),
        Pin("EN"     ,PinType.INPUT,  "CPE_WIRE_L", True),
        Pin("SR"     ,PinType.INPUT,  "CPE_WIRE_L", True),
        Pin("OUT"    ,PinType.OUTPUT, "CPE_WIRE_B", True),
        Pin("RAM_O"  ,PinType.OUTPUT, "CPE_WIRE_B", True),

        Pin("CINX"   ,PinType.INPUT,  "CPE_WIRE_L", True),
        Pin("PINX"   ,PinType.INPUT,  "CPE_WIRE_L", True),
        Pin("CINY1"  ,PinType.INPUT,  "CPE_WIRE_B", True),
        Pin("PINY1"  ,PinType.INPUT,  "CPE_WIRE_B", True),
        Pin("CINY2"  ,PinType.INPUT,  "CPE_WIRE_B", True),
        Pin("PINY2"  ,PinType.INPUT,  "CPE_WIRE_B", True),
        Pin("COUTX"  ,PinType.OUTPUT, "CPE_WIRE_B", True),
        Pin("POUTX"  ,PinType.OUTPUT, "CPE_WIRE_B", True),
        Pin("COUTY1" ,PinType.OUTPUT, "CPE_WIRE_T", True),
        Pin("POUTY1" ,PinType.OUTPUT, "CPE_WIRE_T", True),
        Pin("COUTY2" ,PinType.OUTPUT, "CPE_WIRE_T", True),
        Pin("POUTY2" ,PinType.OUTPUT, "CPE_WIRE_T", True),
    ],

    "GPIO" : [
        Pin("IN1"   , PinType.OUTPUT,"GPIO_WIRE"),
        Pin("IN2"   , PinType.OUTPUT,"GPIO_WIRE"),
        Pin("OUT1"  , PinType.INPUT, "GPIO_WIRE"),
        Pin("OUT2"  , PinType.INPUT, "GPIO_WIRE"),
        Pin("OUT3"  , PinType.INPUT, "GPIO_WIRE"),
        Pin("OUT4"  , PinType.INPUT, "GPIO_WIRE"),
        Pin("DDR"   , PinType.INPUT, "GPIO_WIRE"),
        # Reset is global but no control over it
        #Pin("RESET" , PinType.INPUT, "GPIO_WIRE"),
        Pin("CLOCK1", PinType.INPUT, "GPIO_WIRE"),
        Pin("CLOCK2", PinType.INPUT, "GPIO_WIRE"),
        Pin("CLOCK3", PinType.INPUT, "GPIO_WIRE"),
        Pin("CLOCK4", PinType.INPUT, "GPIO_WIRE"),
    ],
    "BUFG" : [
        Pin("I"     , PinType.INPUT, "BUFG_WIRE", True),
        Pin("O"     , PinType.OUTPUT,"BUFG_WIRE", True),
    ],
    "PLL" : [
        Pin("CLK_REF",             PinType.INPUT, "PLL_WIRE", True),
        Pin("USR_CLK_REF",         PinType.INPUT, "PLL_WIRE"),
        Pin("USR_SEL_A_B",         PinType.INPUT, "PLL_WIRE"),
        Pin("CLK_FEEDBACK",        PinType.INPUT, "PLL_WIRE", True),
        Pin("USR_LOCKED_STDY_RST", PinType.INPUT, "PLL_WIRE"),
        Pin("CLK0",                PinType.OUTPUT,"PLL_WIRE", True),
        Pin("CLK90",               PinType.OUTPUT,"PLL_WIRE", True),
        Pin("CLK180",              PinType.OUTPUT,"PLL_WIRE", True),
        Pin("CLK270",              PinType.OUTPUT,"PLL_WIRE", True),
        Pin("CLK_REF_OUT",         PinType.OUTPUT,"PLL_WIRE", True),
        Pin("USR_PLL_LOCKED_STDY", PinType.OUTPUT,"PLL_WIRE"),
        Pin("USR_PLL_LOCKED",      PinType.OUTPUT,"PLL_WIRE"),
    ],
    "USR_RSTN" : [
        Pin("USR_RSTN", PinType.OUTPUT,"USR_RSTN_WIRE"),
    ],
    "CFG_CTRL" : [
        Pin("DATA[7]", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("DATA[6]", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("DATA[5]", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("DATA[4]", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("DATA[3]", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("DATA[2]", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("DATA[1]", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("DATA[0]", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("CLK", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("EN", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("VALID", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("RECFG", PinType.INPUT,"CFG_CTRL_WIRE"),
    ],
    "RAM" : [
        Pin("C_ADDRA[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRA[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRA[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRA[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRA[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRA[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRA[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRA[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRB[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRB[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRB[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRB[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRB[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRB[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRB[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRB[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("CLKA[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("CLKA[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ENA[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("ENA[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("GLWEA[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("GLWEA[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[16]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[17]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[18]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[19]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[16]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[17]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[18]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[19]", PinType.INPUT,"RAM_WIRE"),
        Pin("CLKA[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("CLKA[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ENA[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("ENA[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("GLWEA[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("GLWEA[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[20]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[21]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[22]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[23]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[24]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[25]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[26]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[27]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[28]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[29]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[30]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[31]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[32]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[33]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[34]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[35]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[36]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[37]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[38]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[39]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[20]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[21]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[22]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[23]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[24]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[25]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[26]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[27]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[28]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[29]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[30]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[31]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[32]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[33]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[34]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[35]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[36]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[37]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[38]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[39]", PinType.INPUT,"RAM_WIRE"),
        Pin("CLKB[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("CLKB[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ENB[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("ENB[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("GLWEB[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("GLWEB[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[16]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[17]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[18]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[19]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[16]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[17]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[18]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[19]", PinType.INPUT,"RAM_WIRE"),
        Pin("CLKB[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("CLKB[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ENB[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("ENB[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("GLWEB[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("GLWEB[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[20]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[21]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[22]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[23]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[24]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[25]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[26]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[27]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[28]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[29]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[30]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[31]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[32]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[33]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[34]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[35]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[36]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[37]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[38]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[39]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[20]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[21]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[22]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[23]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[24]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[25]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[26]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[27]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[28]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[29]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[30]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[31]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[32]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[33]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[34]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[35]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[36]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[37]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[38]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[39]", PinType.INPUT,"RAM_WIRE"),
        Pin("F_RSTN", PinType.INPUT,"RAM_WIRE"),
        Pin("DOA[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[5]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[5]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[6]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[6]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[7]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[7]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[8]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[8]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[9]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[9]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[10]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[10]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[11]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[11]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[12]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[12]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[13]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[13]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[14]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[14]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[15]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[15]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[16]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[16]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[17]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[17]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[18]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[18]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[19]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[19]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[20]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[20]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[21]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[21]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[22]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[22]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[23]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[23]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[24]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[24]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[25]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[25]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[26]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[26]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[27]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[27]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[28]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[28]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[29]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[29]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[30]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[30]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[31]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[31]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[32]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[32]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[33]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[33]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[34]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[34]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[35]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[35]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[36]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[36]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[37]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[37]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[38]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[38]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[39]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[39]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("CLOCKA[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("CLOCKA[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("CLOCKA[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("CLOCKA[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[5]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[5]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[6]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[6]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[7]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[7]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[8]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[8]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[9]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[9]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[10]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[10]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[11]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[11]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[12]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[12]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[13]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[13]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[14]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[14]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[15]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[15]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[16]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[16]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[17]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[17]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[18]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[18]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[19]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[19]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[20]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[20]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[21]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[21]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[22]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[22]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[23]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[23]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[24]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[24]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[25]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[25]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[26]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[26]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[27]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[27]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[28]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[28]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[29]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[29]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[30]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[30]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[31]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[31]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[32]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[32]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[33]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[33]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[34]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[34]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[35]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[35]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[36]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[36]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[37]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[37]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[38]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[38]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[39]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[39]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("CLOCKB[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("CLOCKB[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("CLOCKB[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("CLOCKB[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC1B_ERRA[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC1B_ERRA[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC1B_ERRA[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC1B_ERRA[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC1B_ERRB[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC1B_ERRB[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC1B_ERRB[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC1B_ERRB[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC2B_ERRA[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC2B_ERRA[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC2B_ERRA[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC2B_ERRA[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC2B_ERRB[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC2B_ERRB[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC2B_ERRB[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC2B_ERRB[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("F_FULL[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("F_FULL[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("F_EMPTY[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("F_EMPTY[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("F_AL_FULL[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("F_AL_FULL[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("F_AL_EMPTY[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("F_AL_EMPTY[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ERR[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ERR[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ERR[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ERR[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[5]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[5]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[6]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[6]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[7]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[7]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[8]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[8]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[9]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[9]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[10]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[10]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[11]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[11]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[12]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[12]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[13]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[13]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[14]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[14]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[15]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[15]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[5]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[5]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[6]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[6]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[7]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[7]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[8]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[8]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[9]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[9]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[10]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[10]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[11]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[11]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[12]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[12]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[13]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[13]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[14]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[14]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[15]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[15]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_CAS_WRAO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_CAS_WRAI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_CAS_WRBO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_CAS_WRBI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_CAS_BMAO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_CAS_BMAI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_CAS_BMBO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_CAS_BMBI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_CAS_RDAO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_CAS_RDAI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_CAS_RDBO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_CAS_RDBI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAO[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAO[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAO[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAO[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAO[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAO[5]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAO[6]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAO[7]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAO[8]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAO[9]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAO[10]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAO[11]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAO[12]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAO[13]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAO[14]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAO[15]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAI[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAI[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAI[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAI[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAI[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAI[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAI[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAI[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAI[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAI[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAI[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAI[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAI[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAI[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAI[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAI[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAO[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAO[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAO[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAO[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAO[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAO[5]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAO[6]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAO[7]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAO[8]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAO[9]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAO[10]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAO[11]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAO[12]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAO[13]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAO[14]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRAO[15]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAI[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAI[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAI[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAI[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAI[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAI[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAI[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAI[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAI[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAI[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAI[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAI[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAI[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAI[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAI[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRAI[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBO[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBO[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBO[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBO[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBO[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBO[5]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBO[6]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBO[7]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBO[8]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBO[9]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBO[10]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBO[11]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBO[12]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBO[13]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBO[14]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBO[15]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBI[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBI[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBI[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBI[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBI[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBI[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBI[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBI[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBI[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBI[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBI[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBI[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBI[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBI[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBI[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBI[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBO[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBO[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBO[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBO[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBO[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBO[5]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBO[6]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBO[7]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBO[8]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBO[9]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBO[10]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBO[11]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBO[12]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBO[13]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBO[14]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LADDRBO[15]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBI[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBI[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBI[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBI[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBI[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBI[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBI[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBI[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBI[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBI[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBI[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBI[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBI[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBI[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBI[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UADDRBI[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UA0CLKO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LA0CLKI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UA0ENO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LA0ENI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UA0WEO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LA0WEI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LA0CLKO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UA0CLKI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LA0ENO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UA0ENI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LA0WEO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UA0WEI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UA1CLKO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LA1CLKI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UA1ENO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LA1ENI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UA1WEO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LA1WEI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LA1CLKO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UA1CLKI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LA1ENO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UA1ENI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LA1WEO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UA1WEI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UB0CLKO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LB0CLKI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UB0ENO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LB0ENI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UB0WEO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LB0WEI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LB0CLKO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UB0CLKI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LB0ENO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UB0ENI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LB0WEO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UB0WEI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UB1CLKO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LB1CLKI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UB1ENO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LB1ENI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_UB1WEO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_LB1WEI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LB1CLKO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UB1CLKI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LB1ENO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UB1ENI", PinType.INPUT,"RAM_WIRE"),
        Pin("FORW_LB1WEO", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FORW_UB1WEI", PinType.INPUT,"RAM_WIRE"),
        Pin("CLOCK1", PinType.INPUT,"RAM_WIRE"),
        Pin("CLOCK2", PinType.INPUT,"RAM_WIRE"),
        Pin("CLOCK3", PinType.INPUT,"RAM_WIRE"),
        Pin("CLOCK4", PinType.INPUT,"RAM_WIRE"),
    ],
    "SERDES" : [
        Pin("TX_DETECT_RX_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("PLL_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_CLK_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CLK_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_CLK_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_WE_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_EN_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_PCS_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_PMA_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_PRBS_FORCE_ERR_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_POLARITY_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_8B10B_EN_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_PMA_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_EQA_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_CDR_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_PCS_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_BUF_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_PRBS_CNT_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_EN_EI_DETECTOR_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_COMMA_DETECT_EN_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_SLIDE_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_POLARITY_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_8B10B_EN_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_MCOMMA_ALIGN_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_PCOMMA_ALIGN_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_NOT_IN_TABLE_O[7]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_NOT_IN_TABLE_O[6]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_NOT_IN_TABLE_O[5]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_NOT_IN_TABLE_O[4]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_NOT_IN_TABLE_O[3]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_NOT_IN_TABLE_O[2]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_NOT_IN_TABLE_O[1]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_NOT_IN_TABLE_O[0]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_COMMA_O[7]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_COMMA_O[6]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_COMMA_O[5]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_COMMA_O[4]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_COMMA_O[3]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_COMMA_O[2]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_COMMA_O[1]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_COMMA_O[0]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_ADDR_I[7]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_ADDR_I[6]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_ADDR_I[5]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_ADDR_I[4]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_ADDR_I[3]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_ADDR_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_ADDR_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_ADDR_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_IS_K_I[7]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_IS_K_I[6]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_IS_K_I[5]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_IS_K_I[4]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_IS_K_I[3]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_IS_K_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_IS_K_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_IS_K_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_8B10B_BYPASS_I[7]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_8B10B_BYPASS_I[6]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_8B10B_BYPASS_I[5]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_8B10B_BYPASS_I[4]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_8B10B_BYPASS_I[3]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_8B10B_BYPASS_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_8B10B_BYPASS_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_8B10B_BYPASS_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_8B10B_BYPASS_I[7]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_8B10B_BYPASS_I[6]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_8B10B_BYPASS_I[5]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_8B10B_BYPASS_I[4]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_8B10B_BYPASS_I[3]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_8B10B_BYPASS_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_8B10B_BYPASS_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_8B10B_BYPASS_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPMODE_I[7]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPMODE_I[6]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPMODE_I[5]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPMODE_I[4]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPMODE_I[3]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPMODE_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPMODE_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPMODE_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPVAL_I[7]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPVAL_I[6]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPVAL_I[5]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPVAL_I[4]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPVAL_I[3]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPVAL_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPVAL_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPVAL_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[63]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[62]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[61]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[60]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[59]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[58]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[57]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[56]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[55]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[54]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[53]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[52]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[51]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[50]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[49]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[48]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[47]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[46]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[45]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[44]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[43]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[42]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[41]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[40]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[39]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[38]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[37]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[36]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[35]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[34]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[33]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[32]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[31]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[30]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[29]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[28]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[27]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[26]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[25]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[24]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[23]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[22]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[21]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[20]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[19]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[18]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[17]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[16]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[15]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[14]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[13]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[12]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[11]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[10]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[9]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[8]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[7]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[6]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[5]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[4]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[3]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[15]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[14]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[13]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[12]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[11]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[10]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[9]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[8]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[7]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[6]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[5]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[4]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[3]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[2]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[1]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[0]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[15]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[14]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[13]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[12]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[11]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[10]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[9]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[8]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[7]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[6]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[5]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[4]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[3]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[15]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[14]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[13]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[12]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[11]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[10]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[9]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[8]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[7]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[6]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[5]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[4]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[3]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_K_O[7]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_K_O[6]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_K_O[5]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_K_O[4]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_K_O[3]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_K_O[2]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_K_O[1]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_K_O[0]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DISP_ERR_O[7]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DISP_ERR_O[6]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DISP_ERR_O[5]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DISP_ERR_O[4]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DISP_ERR_O[3]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DISP_ERR_O[2]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DISP_ERR_O[1]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DISP_ERR_O[0]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[63]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[62]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[61]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[60]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[59]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[58]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[57]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[56]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[55]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[54]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[53]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[52]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[51]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[50]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[49]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[48]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[47]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[46]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[45]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[44]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[43]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[42]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[41]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[40]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[39]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[38]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[37]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[36]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[35]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[34]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[33]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[32]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[31]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[30]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[29]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[28]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[27]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[26]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[25]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[24]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[23]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[22]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[21]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[20]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[19]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[18]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[17]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[16]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[15]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[14]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[13]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[12]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[11]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[10]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[9]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[8]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[7]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[6]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[5]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[4]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[3]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[2]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[1]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[0]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("TX_DETECT_RX_DONE_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("TX_DETECT_RX_PRESENT_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CLK_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("PLL_CLK_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("TX_BUF_ERR_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("TX_RESET_DONE_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_RDY_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_PRBS_ERR_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_BUF_ERR_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_BYTE_IS_ALIGNED_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_BYTE_REALIGN_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_RESET_DONE_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_EI_EN_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("LOOPBACK_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("LOOPBACK_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("LOOPBACK_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_PRBS_SEL_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_PRBS_SEL_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_PRBS_SEL_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_PRBS_SEL_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_PRBS_SEL_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_PRBS_SEL_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_POWER_DOWN_N_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_POWER_DOWN_N_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_ELEC_IDLE_I", PinType.INPUT,"SERDES_WIRE"),
    ],
}

def get_groups_for_type(type):
    groups = []
    def create_group(name, type):
        groups.append(Group(name,type))

    if "CPE" in type:
        # CPE
        for p in range(1,13):
            create_group(f"IM_P{p:02d}", "IM")
            if "OM" in type and p>=9:
                create_group(f"OM_P{p:02d}", "OM")
    if "SB_BIG" in type:
        # SB_BIG
        for p in range(1,13):
            create_group(f"SB_BIG_P{p:02d}", "SB_BIG")
    if "SB_SML" in type:
        # SB_SML
        for p in range(1,13):
            create_group(f"SB_SML_P{p:02d}", "SB_SML")
    #if "GPIO" in type:
    #    # GPIO
    if "IOES" in type:
        # IOES
        create_group("IOES", "IOES")
    if "LES" in type:
        # LES
        create_group("LES", "LES")
    if "RES" in type:
        # RES
        create_group("RES", "RES")
    if "TES" in type:
        # TES
        create_group("TES", "TES")
    if "BES" in type:
        # BES
        create_group("BES", "BES")
    return groups

def get_primitives_for_type(type):
    primitives = []
    if "CPE" in type:
        primitives.append(Primitive("CPE_HALF_U","CPE_HALF_U",0))
        primitives.append(Primitive("CPE_HALF_L","CPE_HALF_L",1))
    if "RAM" in type:
        primitives.append(Primitive("RAM","RAM",4))
    if "SERDES" in type:
        primitives.append(Primitive("SERDES","SERDES",4))
    if "GPIO" in type:
        primitives.append(Primitive("GPIO","GPIO",0))
    if "PLL" in type:
        primitives.append(Primitive("BUFG0","BUFG",0))
        primitives.append(Primitive("BUFG1","BUFG",1))
        primitives.append(Primitive("BUFG2","BUFG",2))
        primitives.append(Primitive("BUFG3","BUFG",3))
        primitives.append(Primitive("PLL0","PLL",4))
        primitives.append(Primitive("PLL1","PLL",5))
        primitives.append(Primitive("PLL2","PLL",6))
        primitives.append(Primitive("PLL3","PLL",7))
    if "CFG_CTRL" in type:
        primitives.append(Primitive("CFG_CTRL","CFG_CTRL",2))
        primitives.append(Primitive("USR_RSTN","USR_RSTN",3))
    return primitives

def get_primitive_pins(bel):
    return PRIMITIVES_PINS[bel]

def get_pin_connection_name(prim, pin):
    if prim.type == "BUFG":
        if pin.dir == PinType.INPUT:
            return f"GLBOUT.CLK_SEL_INT_{prim.z}"
        else:
            return f"GLBOUT.GLB{prim.z}"
    elif prim.type == "PLL":
        if pin.name == "CLK_REF":
            return f"CLKIN.CLK_REF_{prim.z - 4}"
        elif pin.name == "CLK0":
            return f"GLBOUT.CLK0_{prim.z - 4}"
        elif pin.name == "CLK90":
            return f"GLBOUT.CLK90_{prim.z - 4}"
        elif pin.name == "CLK180":
            return f"GLBOUT.CLK180_{prim.z - 4}"
        elif pin.name == "CLK270":
            return f"GLBOUT.CLK270_{prim.z - 4}"
        elif pin.name == "CLK_REF_OUT":
            return f"GLBOUT.CLK_REF_OUT{prim.z - 4}"
        elif pin.name == "CLK_FEEDBACK":
            return f"GLBOUT.CLK_FB{prim.z - 4}"
    elif prim.type == "CPE_HALF_U":
        match pin.name:
            case "OUT":
                return "CPE.OUT2"
            case "IN1":
                return "CPE.IN1_int"
            case "IN2":
                return "CPE.IN2_int"
            case "IN3":
                return "CPE.IN3_int"
            case "IN4":
                return "CPE.IN4_int"
            case "RAM_O":
                return "CPE.RAM_O2"
            case "RAM_I":
                return "CPE.RAM_I2"
            case _:
                return f"CPE.{pin.name}"
    elif prim.type == "CPE_HALF_L":
        match pin.name:
            case "OUT":
                return "CPE.OUT1"
            case "IN1":
                return "CPE.IN5_int"
            case "IN2":
                return "CPE.IN6_int"
            case "IN3":
                return "CPE.IN7_int"
            case "IN4":
                return "CPE.IN8_int"
            case "RAM_O":
                return "CPE.RAM_O1"
            case "RAM_I":
                return "CPE.RAM_I1"
            case _:
                return f"CPE.{pin.name}"
    return f"{prim.name}.{pin.name}"

def get_endpoints_for_type(type):
    wires = []
    def create_wire(name, type):
        wires.append(Endpoint(name,type))

    for prim in get_primitives_for_type(type):
        for pin in get_primitive_pins(prim.type):
            if not pin.use_alias_conn:
                create_wire(f"{prim.name}.{pin.name}", type=f"{pin.wire_type}")

    if "CPE" in type:
        create_wire("CPE.RAM_I1" , type="CPE_WIRE_L")
        create_wire("CPE.RAM_I2" , type="CPE_WIRE_L")
        create_wire("CPE.IN1"    , type="CPE_WIRE_L")
        create_wire("CPE.IN2"    , type="CPE_WIRE_L")
        create_wire("CPE.IN3"    , type="CPE_WIRE_L")
        create_wire("CPE.IN4"    , type="CPE_WIRE_L")
        create_wire("CPE.IN5"    , type="CPE_WIRE_L")
        create_wire("CPE.IN6"    , type="CPE_WIRE_L")
        create_wire("CPE.IN7"    , type="CPE_WIRE_L")
        create_wire("CPE.IN8"    , type="CPE_WIRE_L")
        create_wire("CPE.IN1_int", type="CPE_WIRE_INT")
        create_wire("CPE.IN2_int", type="CPE_WIRE_INT")
        create_wire("CPE.IN3_int", type="CPE_WIRE_INT")
        create_wire("CPE.IN4_int", type="CPE_WIRE_INT")
        create_wire("CPE.IN5_int", type="CPE_WIRE_INT")
        create_wire("CPE.IN6_int", type="CPE_WIRE_INT")
        create_wire("CPE.IN7_int", type="CPE_WIRE_INT")
        create_wire("CPE.IN8_int", type="CPE_WIRE_INT")
        create_wire("CPE.CLK"    , type="CPE_WIRE_L")
        create_wire("CPE.EN"     , type="CPE_WIRE_L")
        create_wire("CPE.SR"     , type="CPE_WIRE_L")
        create_wire("CPE.OUT1"   , type="CPE_WIRE_B")
        create_wire("CPE.OUT2"   , type="CPE_WIRE_B")
        create_wire("CPE.RAM_O1" , type="CPE_WIRE_B")
        create_wire("CPE.RAM_O2" , type="CPE_WIRE_B")
        create_wire("CPE.CINX"   , type="CPE_WIRE_L")
        create_wire("CPE.PINX"   , type="CPE_WIRE_L")
        create_wire("CPE.CINY1"  , type="CPE_WIRE_B")
        create_wire("CPE.PINY1"  , type="CPE_WIRE_B")
        create_wire("CPE.CINY2"  , type="CPE_WIRE_B")
        create_wire("CPE.PINY2"  , type="CPE_WIRE_B")
        create_wire("CPE.COUTX"  , type="CPE_WIRE_B")
        create_wire("CPE.POUTX"  , type="CPE_WIRE_B")
        create_wire("CPE.COUTY1" , type="CPE_WIRE_T")
        create_wire("CPE.POUTY1" , type="CPE_WIRE_T")
        create_wire("CPE.COUTY2" , type="CPE_WIRE_T")
        create_wire("CPE.POUTY2" , type="CPE_WIRE_T")
        for p in range(1,13):
            plane = f"{p:02d}"
            for i in range(8):
                create_wire(f"IM.P{plane}.D{i}", type="IM_WIRE")
            create_wire(f"IM.P{plane}.Y", type="IM_WIRE")
            if "OM" in type and p>=9:
                for i in range(4):
                    create_wire(f"OM.P{plane}.D{i}", type="OM_WIRE")
                create_wire(f"OM.P{plane}.Y", type="OM_WIRE")

    if "SB_BIG" in type:
        for p in range(1,13):
            plane = f"{p:02d}"
            create_wire(f"SB_BIG.P{plane}.D0", type="SB_BIG_WIRE")
            for i in range(1,5):
                create_wire(f"SB_BIG.P{plane}.D2_{i}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.D3_{i}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.D4_{i}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.D5_{i}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.D6_{i}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.D7_{i}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.Y{i}", type="SB_BIG_WIRE")

            create_wire(f"SB_BIG.P{plane}.YDIAG", type="SB_BIG_WIRE")
            create_wire(f"SB_BIG.P{plane}.X34", type="SB_BIG_WIRE")
            create_wire(f"SB_BIG.P{plane}.X14", type="SB_BIG_WIRE")
            create_wire(f"SB_BIG.P{plane}.X12", type="SB_BIG_WIRE")
            create_wire(f"SB_BIG.P{plane}.X23", type="SB_BIG_WIRE")

            for i in range(1,5):
                create_wire(f"SB_DRIVE.P{plane}.D{i}.IN", type="SB_DRIVE_WIRE")
                create_wire(f"SB_DRIVE.P{plane}.D{i}.OUT", type="SB_DRIVE_WIRE")
                create_wire(f"SB_DRIVE.P{plane}.D{i}.OUT_NOINV", type="SB_DRIVE_INT_WIRE")

    if "SB_SML" in type:
        for p in range(1,13):
            plane = f"{p:02d}"
            create_wire(f"SB_SML.P{plane}.D0", type="SB_SML_WIRE")
            for i in range(1,5):
                create_wire(f"SB_SML.P{plane}.D2_{i}", type="SB_SML_WIRE")
                create_wire(f"SB_SML.P{plane}.D3_{i}", type="SB_SML_WIRE")
                create_wire(f"SB_SML.P{plane}.Y{i}", type="SB_SML_WIRE")
                create_wire(f"SB_SML.P{plane}.Y{i}_int", type="SB_SML_WIRE")

            create_wire(f"SB_SML.P{plane}.YDIAG", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.YDIAG_int", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.X34", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.X14", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.X12", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.X23", type="SB_SML_WIRE")

    if "IOES" in type:
        create_wire("IOES.IO_IN1", type="IOES_WIRE")
        create_wire("IOES.IO_IN2", type="IOES_WIRE")
        for p in range(1,13):
            plane = f"{p:02d}"
            create_wire(f"IOES.SB_IN_{plane}", type="IOES_WIRE")
            create_wire(f"IOES.ALTIN_{plane}", type="IOES_WIRE")

    if "LES" in type:
        for p in range(1,9):
            create_wire(f"LES.SB_Y3.P{p}", type="LES_WIRE")
            create_wire(f"LES.MDIE1.P{p}", type="LES_WIRE")
        for i in range(4):
            create_wire(f"LES.CLOCK{i}", type="LES_WIRE")
        create_wire("LES.CPE_CINX", type="LES_WIRE")
        create_wire("LES.CPE_PINX", type="LES_WIRE")
        # Internal wires
        create_wire("LES.SB_Y3_SEL1_int", type="LES_INT_WIRE")
        create_wire("LES.MDIE1_SEL1_int", type="LES_INT_WIRE")
        create_wire("LES.CLOCK_SEL1_int", type="LES_INT_WIRE")
        create_wire("LES.SB_Y3_SEL2_int", type="LES_INT_WIRE")
        create_wire("LES.MDIE1_SEL2_int", type="LES_INT_WIRE")
        create_wire("LES.CLOCK_SEL2_int", type="LES_INT_WIRE")

    if "BES" in type:
        for p in range(1,9):
            create_wire(f"BES.SB_Y4.P{p}", type="BES_WIRE")
            create_wire(f"BES.MDIE2.P{p}", type="BES_WIRE")
        for i in range(4):
            create_wire(f"BES.CLOCK{i}", type="BES_WIRE")
        create_wire("BES.P_CINY1", type="BES_WIRE")
        create_wire("BES.P_PINY1", type="BES_WIRE")
        create_wire("BES.P_CINY2", type="BES_WIRE")
        create_wire("BES.P_PINY2", type="BES_WIRE")
        create_wire("BES.CPE_CINY1", type="BES_WIRE")
        create_wire("BES.CPE_PINY1", type="BES_WIRE")
        create_wire("BES.CPE_CINY2", type="BES_WIRE")
        create_wire("BES.CPE_PINY2", type="BES_WIRE")
        # Internal wires
        create_wire("BES.SB_Y4_SEL1_int", type="BES_INT_WIRE")
        create_wire("BES.MDIE2_SEL1_int", type="BES_INT_WIRE")
        create_wire("BES.CLOCK_SEL1_int", type="BES_INT_WIRE")
        create_wire("BES.SB_Y4_SEL2_int", type="BES_INT_WIRE")
        create_wire("BES.MDIE2_SEL2_int", type="BES_INT_WIRE")
        create_wire("BES.CLOCK_SEL2_int", type="BES_INT_WIRE")
        create_wire("BES.SB_Y4_SEL3_int", type="BES_INT_WIRE")
        create_wire("BES.MDIE2_SEL3_int", type="BES_INT_WIRE")
        create_wire("BES.CLOCK_SEL3_int", type="BES_INT_WIRE")
        create_wire("BES.SB_Y4_SEL4_int", type="BES_INT_WIRE")
        create_wire("BES.MDIE2_SEL4_int", type="BES_INT_WIRE")
        create_wire("BES.CLOCK_SEL4_int", type="BES_INT_WIRE")
        create_wire("BES.CPE_CINY1_int", type="BES_INT_WIRE")
        create_wire("BES.CPE_PINY1_int", type="BES_INT_WIRE")
        create_wire("BES.CPE_CINY2_int", type="BES_INT_WIRE")
        create_wire("BES.CPE_PINY2_int", type="BES_INT_WIRE")

    if "RES" in type:
        create_wire("RES.CPE_RAM_O1", type="RES_WIRE")
        create_wire("RES.CPE_RAM_O2", type="RES_WIRE")
        create_wire("RES.CPE_COUTX", type="RES_WIRE")
        create_wire("RES.CPE_POUTX", type="RES_WIRE")
        for p in range(1,9):
            create_wire(f"RES.SB_Y1.P{p}", type="RES_WIRE")
            create_wire(f"RES.MDIE1.P{p}", type="RES_WIRE")
        for i in range(4):
            create_wire(f"RES.CLOCK{i}", type="RES_WIRE")
        # Internal wires
        create_wire("RES.SIG_SEL1_int", type="RES_INT_WIRE")
        create_wire("RES.SIG_SEL2_int", type="RES_INT_WIRE")
        create_wire("RES.SIG_SEL3_int", type="RES_INT_WIRE")
        create_wire("RES.SIG_SEL4_int", type="RES_INT_WIRE")

    if "TES" in type:
        create_wire("TES.CPE_RAM_O1", type="TES_WIRE")
        create_wire("TES.CPE_RAM_O2", type="TES_WIRE")
        create_wire("TES.CPE_COUTY1", type="TES_WIRE")
        create_wire("TES.CPE_POUTY1", type="TES_WIRE")
        create_wire("TES.CPE_COUTY2", type="TES_WIRE")
        create_wire("TES.CPE_POUTY2", type="TES_WIRE")
        for p in range(1,9):
            create_wire(f"TES.SB_Y2.P{p}", type="TES_WIRE")
            create_wire(f"TES.MDIE2.P{p}", type="TES_WIRE")
        for i in range(4):
            create_wire(f"TES.CLOCK{i}", type="TES_WIRE")
        # Internal wires
        create_wire("TES.SIG_SEL1_int", type="TES_INT_WIRE")
        create_wire("TES.SIG_SEL2_int", type="TES_INT_WIRE")
        create_wire("TES.SIG_SEL3_int", type="TES_INT_WIRE")
        create_wire("TES.SIG_SEL4_int", type="TES_INT_WIRE")

    if "PLL" in type:
        # CLKIN
        create_wire("CLKIN.CLK0", type="CLKIN_WIRE")
        create_wire("CLKIN.CLK1", type="CLKIN_WIRE")
        create_wire("CLKIN.CLK2", type="CLKIN_WIRE")
        create_wire("CLKIN.CLK3", type="CLKIN_WIRE")
        create_wire("CLKIN.SER_CLK", type="CLKIN_WIRE")
        create_wire("CLKIN.CLK_REF_INT0", type="CLKIN_INT_WIRE") # internal
        create_wire("CLKIN.CLK_REF_INT1", type="CLKIN_INT_WIRE") # internal
        create_wire("CLKIN.CLK_REF_INT2", type="CLKIN_INT_WIRE") # internal
        create_wire("CLKIN.CLK_REF_INT3", type="CLKIN_INT_WIRE") # internal
        create_wire("CLKIN.CLK_REF_0", type="CLKIN_WIRE")
        create_wire("CLKIN.CLK_REF_1", type="CLKIN_WIRE")
        create_wire("CLKIN.CLK_REF_2", type="CLKIN_WIRE")
        create_wire("CLKIN.CLK_REF_3", type="CLKIN_WIRE")
        # GLBOUT
        create_wire("GLBOUT.CLK0_0", type="GLBOUT_WIRE")
        create_wire("GLBOUT.CLK90_0", type="GLBOUT_WIRE")
        create_wire("GLBOUT.CLK180_0", type="GLBOUT_WIRE")
        create_wire("GLBOUT.CLK270_0", type="GLBOUT_WIRE")
        create_wire("GLBOUT.CLK_INT_0", type="GLBOUT_INT_WIRE")
        create_wire("GLBOUT.CLK_SEL_INT_0", type="GLBOUT_INT_WIRE")
        create_wire("GLBOUT.CLK_REF_OUT0", type="GLBOUT_WIRE")
        create_wire("GLBOUT.USR_GLB0", type="GLBOUT_WIRE")
        create_wire("GLBOUT.GLB0", type="GLBOUT_WIRE")
        create_wire("GLBOUT.FB_INT_0", type="GLBOUT_INT_WIRE")
        create_wire("GLBOUT.USR_FB0", type="GLBOUT_WIRE")
        create_wire("GLBOUT.CLK_FB0", type="GLBOUT_WIRE")

        create_wire("GLBOUT.CLK0_1", type="GLBOUT_WIRE")
        create_wire("GLBOUT.CLK90_1", type="GLBOUT_WIRE")
        create_wire("GLBOUT.CLK180_1", type="GLBOUT_WIRE")
        create_wire("GLBOUT.CLK270_1", type="GLBOUT_WIRE")
        create_wire("GLBOUT.CLK_INT_1", type="GLBOUT_INT_WIRE")
        create_wire("GLBOUT.CLK_SEL_INT_1", type="GLBOUT_INT_WIRE")
        create_wire("GLBOUT.CLK_REF_OUT1", type="GLBOUT_WIRE")
        create_wire("GLBOUT.USR_GLB1", type="GLBOUT_WIRE")
        create_wire("GLBOUT.GLB1", type="GLBOUT_WIRE")
        create_wire("GLBOUT.FB_INT_1", type="GLBOUT_INT_WIRE")
        create_wire("GLBOUT.USR_FB1", type="GLBOUT_WIRE")
        create_wire("GLBOUT.CLK_FB1", type="GLBOUT_WIRE")

        create_wire("GLBOUT.CLK0_2", type="GLBOUT_WIRE")
        create_wire("GLBOUT.CLK90_2", type="GLBOUT_WIRE")
        create_wire("GLBOUT.CLK180_2", type="GLBOUT_WIRE")
        create_wire("GLBOUT.CLK270_2", type="GLBOUT_WIRE")
        create_wire("GLBOUT.CLK_INT_2", type="GLBOUT_INT_WIRE")
        create_wire("GLBOUT.CLK_SEL_INT_2", type="GLBOUT_INT_WIRE")
        create_wire("GLBOUT.CLK_REF_OUT2", type="GLBOUT_WIRE")
        create_wire("GLBOUT.USR_GLB2", type="GLBOUT_WIRE")
        create_wire("GLBOUT.GLB2", type="GLBOUT_WIRE")
        create_wire("GLBOUT.FB_INT_2", type="GLBOUT_INT_WIRE")
        create_wire("GLBOUT.USR_FB2", type="GLBOUT_WIRE")
        create_wire("GLBOUT.CLK_FB2", type="GLBOUT_WIRE")

        create_wire("GLBOUT.CLK0_3", type="GLBOUT_WIRE")
        create_wire("GLBOUT.CLK90_3", type="GLBOUT_WIRE")
        create_wire("GLBOUT.CLK180_3", type="GLBOUT_WIRE")
        create_wire("GLBOUT.CLK270_3", type="GLBOUT_WIRE")
        create_wire("GLBOUT.CLK_INT_3", type="GLBOUT_INT_WIRE")
        create_wire("GLBOUT.CLK_SEL_INT_3", type="GLBOUT_INT_WIRE")
        create_wire("GLBOUT.CLK_REF_OUT3", type="GLBOUT_WIRE")
        create_wire("GLBOUT.USR_GLB3", type="GLBOUT_WIRE")
        create_wire("GLBOUT.GLB3", type="GLBOUT_WIRE")
        create_wire("GLBOUT.FB_INT_3", type="GLBOUT_INT_WIRE")
        create_wire("GLBOUT.USR_FB3", type="GLBOUT_WIRE")
        create_wire("GLBOUT.CLK_FB3", type="GLBOUT_WIRE")

    return wires

def get_mux_connections_for_type(type):
    muxes = []
    def create_mux(src, dst, bits, value, invert, name = None, visible = True, config = False):
        name = dst if name is None else name
        muxes.append(MUX(src, dst, name, bits, value, invert, visible, config))

    if "CPE" in type:
        # CPE
        for i in range(1,9):
            create_mux(f"CPE.IN{i}", f"CPE.IN{i}_int", 0, 0, False, None, False)
        create_mux("CPE.PINY1", "CPE.IN2_int", 1, 1, False, "CPE.C_I1")
        create_mux("CPE.CINX",  "CPE.IN4_int", 1, 1, False, "CPE.C_I2")
        create_mux("CPE.PINY1", "CPE.IN6_int", 1, 1, False, "CPE.C_I3")
        create_mux("CPE.PINX",  "CPE.IN8_int", 1, 1, False, "CPE.C_I4")
        for p in range(1,13):
            plane = f"{p:02d}"
            for i in range(8):
                create_mux(f"IM.P{plane}.D{i}", f"IM.P{plane}.Y", 3, i, True, f"IM.P{plane}")
            if "OM" in type and p>=9:
                for i in range(4):
                    create_mux(f"OM.P{plane}.D{i}", f"OM.P{plane}.Y", 2, i, True, f"OM.P{plane}")

    if "SB_BIG" in type:
        # SB_BIG
        for p in range(1,13):
            plane = f"{p:02d}"
            # Per Y output mux
            for i in range(1,5):
                create_mux(f"SB_BIG.P{plane}.D0",     f"SB_BIG.P{plane}.Y{i}", 3, 0, True)
                create_mux(f"SB_BIG.P{plane}.YDIAG",  f"SB_BIG.P{plane}.Y{i}", 3, 1, True)
                create_mux(f"SB_BIG.P{plane}.D2_{i}", f"SB_BIG.P{plane}.Y{i}", 3, 2, True)
                create_mux(f"SB_BIG.P{plane}.D3_{i}", f"SB_BIG.P{plane}.Y{i}", 3, 3, True)
                create_mux(f"SB_BIG.P{plane}.D4_{i}", f"SB_BIG.P{plane}.Y{i}", 3, 4, True)
                create_mux(f"SB_BIG.P{plane}.D5_{i}", f"SB_BIG.P{plane}.Y{i}", 3, 5, True)
                create_mux(f"SB_BIG.P{plane}.D6_{i}", f"SB_BIG.P{plane}.Y{i}", 3, 6, True)
                create_mux(f"SB_BIG.P{plane}.D7_{i}", f"SB_BIG.P{plane}.Y{i}", 3, 7, True)

            # YDIAG output mux
            create_mux(f"SB_BIG.P{plane}.Y1",  f"SB_BIG.P{plane}.YDIAG", 3, 0, True)
            create_mux(f"SB_BIG.P{plane}.Y2",  f"SB_BIG.P{plane}.YDIAG", 3, 1, True)
            create_mux(f"SB_BIG.P{plane}.Y3",  f"SB_BIG.P{plane}.YDIAG", 3, 2, True)
            create_mux(f"SB_BIG.P{plane}.Y4",  f"SB_BIG.P{plane}.YDIAG", 3, 3, True)
            create_mux(f"SB_BIG.P{plane}.X34", f"SB_BIG.P{plane}.YDIAG", 3, 4, True)
            create_mux(f"SB_BIG.P{plane}.X14", f"SB_BIG.P{plane}.YDIAG", 3, 5, True)
            create_mux(f"SB_BIG.P{plane}.X12", f"SB_BIG.P{plane}.YDIAG", 3, 6, True)
            create_mux(f"SB_BIG.P{plane}.X23", f"SB_BIG.P{plane}.YDIAG", 3, 7, True)

            for i in range(1,5):
                create_mux(f"SB_DRIVE.P{plane}.D{i}.IN", f"SB_DRIVE.P{plane}.D{i}.OUT", 1, 1, True, f"SB_DRIVE.P{plane}.D{i}")
                create_mux(f"SB_DRIVE.P{plane}.D{i}.IN", f"SB_DRIVE.P{plane}.D{i}.OUT_NOINV", 1, 1, False, f"SB_DRIVE.P{plane}.D{i}")

    if "SB_SML" in type:
        # SB_SML
        for p in range(1,13):
            plane = f"{p:02d}"
            # Per Y output mux
            for i in range(1,5):
                create_mux(f"SB_SML.P{plane}.D0",       f"SB_SML.P{plane}.Y{i}_int", 2, 0, False, f"SB_SML.P{plane}.Y{i}")
                create_mux(f"SB_SML.P{plane}.YDIAG_int",f"SB_SML.P{plane}.Y{i}_int", 2, 1, False, f"SB_SML.P{plane}.Y{i}")
                create_mux(f"SB_SML.P{plane}.D2_{i}",   f"SB_SML.P{plane}.Y{i}_int", 2, 2, False, f"SB_SML.P{plane}.Y{i}")
                create_mux(f"SB_SML.P{plane}.D3_{i}",   f"SB_SML.P{plane}.Y{i}_int", 2, 3, False, f"SB_SML.P{plane}.Y{i}")

            # YDIAG output mux
            create_mux(f"SB_SML.P{plane}.Y1_int", f"SB_SML.P{plane}.YDIAG_int", 3, 0, False, f"SB_SML.P{plane}.YDIAG")
            create_mux(f"SB_SML.P{plane}.Y2_int", f"SB_SML.P{plane}.YDIAG_int", 3, 1, False, f"SB_SML.P{plane}.YDIAG")
            create_mux(f"SB_SML.P{plane}.Y3_int", f"SB_SML.P{plane}.YDIAG_int", 3, 2, False, f"SB_SML.P{plane}.YDIAG")
            create_mux(f"SB_SML.P{plane}.Y4_int", f"SB_SML.P{plane}.YDIAG_int", 3, 3, False, f"SB_SML.P{plane}.YDIAG")
            create_mux(f"SB_SML.P{plane}.X34",    f"SB_SML.P{plane}.YDIAG_int", 3, 4, False, f"SB_SML.P{plane}.YDIAG")
            create_mux(f"SB_SML.P{plane}.X14",    f"SB_SML.P{plane}.YDIAG_int", 3, 5, False, f"SB_SML.P{plane}.YDIAG")
            create_mux(f"SB_SML.P{plane}.X12",    f"SB_SML.P{plane}.YDIAG_int", 3, 6, False, f"SB_SML.P{plane}.YDIAG")
            create_mux(f"SB_SML.P{plane}.X23",    f"SB_SML.P{plane}.YDIAG_int", 3, 7, False, f"SB_SML.P{plane}.YDIAG")

            create_mux(f"SB_SML.P{plane}.Y1_int",    f"SB_SML.P{plane}.Y1",    1, 1, True, f"SB_SML.P{plane}.Y1_INT", False)
            create_mux(f"SB_SML.P{plane}.Y2_int",    f"SB_SML.P{plane}.Y2",    1, 1, True, f"SB_SML.P{plane}.Y2_INT", False)
            create_mux(f"SB_SML.P{plane}.Y3_int",    f"SB_SML.P{plane}.Y3",    1, 1, True, f"SB_SML.P{plane}.Y3_INT", False)
            create_mux(f"SB_SML.P{plane}.Y4_int",    f"SB_SML.P{plane}.Y4",    1, 1, True, f"SB_SML.P{plane}.Y4_INT", False)
            create_mux(f"SB_SML.P{plane}.YDIAG_int", f"SB_SML.P{plane}.YDIAG", 1, 1, True, f"SB_SML.P{plane}.YDIAG_INT", False)

    #if "GPIO" in type:
    #    # GPIO
    if "IOES" in type:
        # IOES
        for p in range(1,13):
            plane = f"{p:02d}"
            io_in = 1 if p % 2 else 2
            create_mux(f"IOES.IO_IN{io_in}", f"IOES.SB_IN_{plane}", 1, 0, False)
            create_mux(f"IOES.ALTIN_{plane}", f"IOES.SB_IN_{plane}", 1, 1, False)

    if "LES" in type:
        for p in range(1,9):
            create_mux(f"LES.SB_Y3.P{p}", "LES.SB_Y3_SEL1_int", 3, p-1, False, "LES.SB_Y3_SEL1")
            create_mux(f"LES.MDIE1.P{p}", "LES.MDIE1_SEL1_int", 3, p-1, False, "LES.MDIE1_SEL1")
            create_mux(f"LES.SB_Y3.P{p}", "LES.SB_Y3_SEL2_int", 3, p-1, False, "LES.SB_Y3_SEL2")
            create_mux(f"LES.MDIE1.P{p}", "LES.MDIE1_SEL2_int", 3, p-1, False, "LES.MDIE1_SEL2")
        for i in range(4):
            create_mux(f"LES.CLOCK{i}", "LES.CLOCK_SEL1_int", 2, i, False, "LES.CLOCK_SEL1")
            create_mux(f"LES.CLOCK{i}", "LES.CLOCK_SEL2_int", 2, i, False, "LES.CLOCK_SEL2")

        create_mux("LES.SB_Y3_SEL1_int", "LES.CPE_CINX", 2, 1, False, "LES.CINX_SEL")
        create_mux("LES.MDIE1_SEL1_int", "LES.CPE_CINX", 2, 2, False, "LES.CINX_SEL")
        create_mux("LES.CLOCK_SEL1_int", "LES.CPE_CINX", 2, 3, False, "LES.CINX_SEL")

        create_mux("LES.SB_Y3_SEL2_int", "LES.CPE_PINX", 2, 1, False, "LES.PINX_SEL")
        create_mux("LES.MDIE1_SEL2_int", "LES.CPE_PINX", 2, 2, False, "LES.PINX_SEL")
        create_mux("LES.CLOCK_SEL2_int", "LES.CPE_PINX", 2, 3, False, "LES.PINX_SEL")

    if "BES" in type:
        for p in range(1,9):
            create_mux(f"BES.SB_Y4.P{p}", "BES.SB_Y4_SEL1_int", 3, p-1, False, "BES.SB_Y4_SEL1")
            create_mux(f"BES.MDIE2.P{p}", "BES.MDIE2_SEL1_int", 3, p-1, False, "BES.MDIE2_SEL1")
            create_mux(f"BES.SB_Y4.P{p}", "BES.SB_Y4_SEL2_int", 3, p-1, False, "BES.SB_Y4_SEL2")
            create_mux(f"BES.MDIE2.P{p}", "BES.MDIE2_SEL2_int", 3, p-1, False, "BES.MDIE2_SEL2")
            create_mux(f"BES.SB_Y4.P{p}", "BES.SB_Y4_SEL3_int", 3, p-1, False, "BES.SB_Y4_SEL3")
            create_mux(f"BES.MDIE2.P{p}", "BES.MDIE2_SEL3_int", 3, p-1, False, "BES.MDIE2_SEL3")
            create_mux(f"BES.SB_Y4.P{p}", "BES.SB_Y4_SEL4_int", 3, p-1, False, "BES.SB_Y4_SEL4")
            create_mux(f"BES.MDIE2.P{p}", "BES.MDIE2_SEL4_int", 3, p-1, False, "BES.MDIE2_SEL4")
        for i in range(4):
            create_mux(f"BES.CLOCK{i}", "BES.CLOCK_SEL1_int", 2, i, False, "BES.CLOCK_SEL1")
            create_mux(f"BES.CLOCK{i}", "BES.CLOCK_SEL2_int", 2, i, False, "BES.CLOCK_SEL2")
            create_mux(f"BES.CLOCK{i}", "BES.CLOCK_SEL3_int", 2, i, False, "BES.CLOCK_SEL3")
            create_mux(f"BES.CLOCK{i}", "BES.CLOCK_SEL4_int", 2, i, False, "BES.CLOCK_SEL4")

        create_mux("BES.SB_Y4_SEL1_int", "BES.CPE_CINY1_int", 2, 1, False, "BES.CINY1_SEL")
        create_mux("BES.MDIE2_SEL1_int", "BES.CPE_CINY1_int", 2, 2, False, "BES.CINY1_SEL")
        create_mux("BES.CLOCK_SEL1_int", "BES.CPE_CINY1_int", 2, 3, False, "BES.CINY1_SEL")
        create_mux("BES.SB_Y4_SEL2_int", "BES.CPE_PINY1_int", 2, 1, False, "BES.PINY1_SEL")
        create_mux("BES.MDIE2_SEL2_int", "BES.CPE_PINY1_int", 2, 2, False, "BES.PINY1_SEL")
        create_mux("BES.CLOCK_SEL2_int", "BES.CPE_PINY1_int", 2, 3, False, "BES.PINY1_SEL")
        create_mux("BES.SB_Y4_SEL3_int", "BES.CPE_CINY2_int", 2, 1, False, "BES.CINY2_SEL")
        create_mux("BES.MDIE2_SEL3_int", "BES.CPE_CINY2_int", 2, 2, False, "BES.CINY2_SEL")
        create_mux("BES.CLOCK_SEL3_int", "BES.CPE_CINY2_int", 2, 3, False, "BES.CINY2_SEL")
        create_mux("BES.SB_Y4_SEL4_int", "BES.CPE_PINY2_int", 2, 1, False, "BES.PINY2_SEL")
        create_mux("BES.MDIE2_SEL4_int", "BES.CPE_PINY2_int", 2, 2, False, "BES.PINY2_SEL")
        create_mux("BES.CLOCK_SEL4_int", "BES.CPE_PINY2_int", 2, 3, False, "BES.PINY2_SEL")

        create_mux("BES.CPE_CINY1_int", "BES.CPE_CINY1",      1, 0, False, "BES.P_CINY1")
        create_mux("BES.P_CINY1",       "BES.CPE_CINY1",      1, 1, False, "BES.P_CINY1")
        create_mux("BES.CPE_PINY1_int", "BES.CPE_PINY1",      1, 0, False, "BES.P_PINY1")
        create_mux("BES.P_PINY1",       "BES.CPE_PINY1",      1, 1, False, "BES.P_PINY1")
        create_mux("BES.CPE_CINY2_int", "BES.CPE_CINY2",      1, 0, False, "BES.P_CINY2")
        create_mux("BES.P_CINY2",       "BES.CPE_CINY2",      1, 1, False, "BES.P_CINY2")
        create_mux("BES.CPE_PINY2_int", "BES.CPE_PINY2",      1, 0, False, "BES.P_PINY2")
        create_mux("BES.P_PINY2",       "BES.CPE_PINY2",      1, 1, False, "BES.P_PINY2")

    if "RES" in type:
        for sel in range(4):
            create_mux("RES.CPE_RAM_O1", f"RES.SIG_SEL{sel+1}_int", 3, 0, False, f"RES.SIG_SEL{sel+1}")
            create_mux("RES.CPE_RAM_O2", f"RES.SIG_SEL{sel+1}_int", 3, 1, False, f"RES.SIG_SEL{sel+1}")
            create_mux("RES.CPE_COUTX",  f"RES.SIG_SEL{sel+1}_int", 3, 2, False, f"RES.SIG_SEL{sel+1}")
            create_mux("RES.CPE_POUTX",  f"RES.SIG_SEL{sel+1}_int", 3, 3, False, f"RES.SIG_SEL{sel+1}")
            for i in range(4):
                create_mux(f"RES.CLOCK{i}", f"RES.SIG_SEL{sel+1}_int", 3, 4 + i, False, f"RES.SIG_SEL{sel+1}")

        for p in range(1,9):
            create_mux(f"RES.SB_Y1.P{p}", f"RES.MDIE1.P{p}", 1, 0, False, f"RES.SEL_MDIE{p}")
            sel = (p - 1) // 2 + 1
            create_mux(f"RES.SIG_SEL{sel}_int", f"RES.MDIE1.P{p}", 1, 1, False, f"RES.SEL_MDIE{p}")

    if "TES" in type:
        for sel in range(4):
            create_mux("TES.CPE_RAM_O1", f"TES.SIG_SEL{sel+1}_int", 3, 0, False, f"TES.SIG_SEL{sel+1}")
            create_mux("TES.CPE_RAM_O2", f"TES.SIG_SEL{sel+1}_int", 3, 1, False, f"TES.SIG_SEL{sel+1}")
            create_mux("TES.CPE_COUTY1", f"TES.SIG_SEL{sel+1}_int", 3, 2, False, f"TES.SIG_SEL{sel+1}")
            create_mux("TES.CPE_POUTY1", f"TES.SIG_SEL{sel+1}_int", 3, 3, False, f"TES.SIG_SEL{sel+1}")
            create_mux("TES.CPE_COUTY2", f"TES.SIG_SEL{sel+1}_int", 3, 4, False, f"TES.SIG_SEL{sel+1}")
            create_mux("TES.CPE_POUTY2", f"TES.SIG_SEL{sel+1}_int", 3, 5, False, f"TES.SIG_SEL{sel+1}")
            clk = 0 if sel < 2 else 2
            create_mux(f"TES.CLOCK{clk+0}", f"TES.SIG_SEL{sel+1}_int", 3, 6, False, f"TES.SIG_SEL{sel+1}")
            create_mux(f"TES.CLOCK{clk+1}", f"TES.SIG_SEL{sel+1}_int", 3, 7, False, f"TES.SIG_SEL{sel+1}")

        for p in range(1,9):
            create_mux(f"TES.SB_Y2.P{p}", f"TES.MDIE2.P{p}", 1, 0, False, f"TES.SEL_MDIE{p}")
            sel = (p - 1) // 2 + 1
            create_mux(f"TES.SIG_SEL{sel}_int", f"TES.MDIE2.P{p}", 1, 1, False, f"TES.SEL_MDIE{p}")

    if "PLL" in type:
        # CLKIN

        create_mux("CLKIN.CLK0", "CLKIN.CLK_REF_INT0", 3, 0, False, "CLKIN.REF0", config=True)
        create_mux("CLKIN.CLK1", "CLKIN.CLK_REF_INT0", 3, 1, False, "CLKIN.REF0", config=True)
        create_mux("CLKIN.CLK2", "CLKIN.CLK_REF_INT0", 3, 2, False, "CLKIN.REF0", config=True)
        create_mux("CLKIN.CLK3", "CLKIN.CLK_REF_INT0", 3, 3, False, "CLKIN.REF0", config=True)
        create_mux("CLKIN.SER_CLK", "CLKIN.CLK_REF_INT0", 3, 4, False, "CLKIN.REF0", config=True)
        create_mux("CLKIN.CLK_REF_INT0", "CLKIN.CLK_REF_0", 1, 0, False, "CLKIN.REF0_INV", config=True)

        create_mux("CLKIN.CLK0", "CLKIN.CLK_REF_INT1", 3, 0, False, "CLKIN.REF1", config=True)
        create_mux("CLKIN.CLK1", "CLKIN.CLK_REF_INT1", 3, 1, False, "CLKIN.REF1", config=True)
        create_mux("CLKIN.CLK2", "CLKIN.CLK_REF_INT1", 3, 2, False, "CLKIN.REF1", config=True)
        create_mux("CLKIN.CLK3", "CLKIN.CLK_REF_INT1", 3, 3, False, "CLKIN.REF1", config=True)
        create_mux("CLKIN.SER_CLK", "CLKIN.CLK_REF_INT1", 3, 4, False, "CLKIN.REF1", config=True)
        create_mux("CLKIN.CLK_REF_INT1", "CLKIN.CLK_REF_1", 1, 0, False, "CLKIN.REF1_INV", config=True)

        create_mux("CLKIN.CLK0", "CLKIN.CLK_REF_INT2", 3, 0, False, "CLKIN.REF2", config=True)
        create_mux("CLKIN.CLK1", "CLKIN.CLK_REF_INT2", 3, 1, False, "CLKIN.REF2", config=True)
        create_mux("CLKIN.CLK2", "CLKIN.CLK_REF_INT2", 3, 2, False, "CLKIN.REF2", config=True)
        create_mux("CLKIN.CLK3", "CLKIN.CLK_REF_INT2", 3, 3, False, "CLKIN.REF2", config=True)
        create_mux("CLKIN.SER_CLK", "CLKIN.CLK_REF_INT2", 3, 4, False, "CLKIN.REF2", config=True)
        create_mux("CLKIN.CLK_REF_INT2", "CLKIN.CLK_REF_2", 1, 0, False, "CLKIN.REF2_INV", config=True)

        create_mux("CLKIN.CLK0", "CLKIN.CLK_REF_INT3", 3, 0, False, "CLKIN.REF3", config=True)
        create_mux("CLKIN.CLK1", "CLKIN.CLK_REF_INT3", 3, 1, False, "CLKIN.REF3", config=True)
        create_mux("CLKIN.CLK2", "CLKIN.CLK_REF_INT3", 3, 2, False, "CLKIN.REF3", config=True)
        create_mux("CLKIN.CLK3", "CLKIN.CLK_REF_INT3", 3, 3, False, "CLKIN.REF3", config=True)
        create_mux("CLKIN.SER_CLK", "CLKIN.CLK_REF_INT3", 3, 4, False, "CLKIN.REF3", config=True)
        create_mux("CLKIN.CLK_REF_INT3", "CLKIN.CLK_REF_3", 1, 0, False, "CLKIN.REF3_INV", config=True)

        # GLBOUT

        create_mux("GLBOUT.CLK_REF_OUT0", "GLBOUT.CLK_INT_0", 3, 0, False, "GLBOUT.GLB0", config=True)
        create_mux("GLBOUT.CLK0_1", "GLBOUT.CLK_INT_0", 3, 1, False, "GLBOUT.GLB0", config=True)
        create_mux("GLBOUT.CLK0_2", "GLBOUT.CLK_INT_0", 3, 2, False, "GLBOUT.GLB0", config=True)
        create_mux("GLBOUT.CLK0_3", "GLBOUT.CLK_INT_0", 3, 3, False, "GLBOUT.GLB0", config=True)
        create_mux("GLBOUT.CLK0_0", "GLBOUT.CLK_INT_0", 3, 4, False, "GLBOUT.GLB0", config=True)
        create_mux("GLBOUT.CLK90_0", "GLBOUT.CLK_INT_0", 3, 5, False, "GLBOUT.GLB0", config=True)
        create_mux("GLBOUT.CLK180_0", "GLBOUT.CLK_INT_0", 3, 6, False, "GLBOUT.GLB0", config=True)
        create_mux("GLBOUT.CLK270_0", "GLBOUT.CLK_INT_0", 3, 7, False, "GLBOUT.GLB0", config=True)

        create_mux("GLBOUT.CLK_INT_0", "GLBOUT.CLK_SEL_INT_0", 1, 0, False, "GLBOUT.USR_GLB0", config=True)
        create_mux("GLBOUT.USR_GLB0", "GLBOUT.CLK_SEL_INT_0", 1, 1, False, "GLBOUT.USR_GLB0", config=True)

        create_mux("GLBOUT.CLK_SEL_INT_0", "GLBOUT.GLB0", 1, 1, False, "GLBOUT.GLB0_EN", config=True)

        create_mux("GLBOUT.GLB0", "GLBOUT.FB_INT_0", 2, 0, False, "GLBOUT.FB0", config=True)
        create_mux("GLBOUT.GLB1", "GLBOUT.FB_INT_0", 2, 1, False, "GLBOUT.FB0", config=True)
        create_mux("GLBOUT.GLB2", "GLBOUT.FB_INT_0", 2, 2, False, "GLBOUT.FB0", config=True)
        create_mux("GLBOUT.GLB3", "GLBOUT.FB_INT_0", 2, 3, False, "GLBOUT.FB0", config=True)

        create_mux("GLBOUT.FB_INT_0", "GLBOUT.CLK_FB0", 1, 0, False, "GLBOUT.USR_FB0", config=True)
        create_mux("GLBOUT.USR_FB0", "GLBOUT.CLK_FB0",  1, 1, False, "GLBOUT.USR_FB0", config=True)


        create_mux("GLBOUT.CLK_REF_OUT1", "GLBOUT.CLK_INT_1", 3, 0, False, "GLBOUT.GLB1", config=True)
        create_mux("GLBOUT.CLK90_0", "GLBOUT.CLK_INT_1", 3, 1, False, "GLBOUT.GLB1", config=True)
        create_mux("GLBOUT.CLK90_2", "GLBOUT.CLK_INT_1", 3, 2, False, "GLBOUT.GLB1", config=True)
        create_mux("GLBOUT.CLK90_3", "GLBOUT.CLK_INT_1", 3, 3, False, "GLBOUT.GLB1", config=True)
        create_mux("GLBOUT.CLK0_1", "GLBOUT.CLK_INT_1", 3, 4, False, "GLBOUT.GLB1", config=True)
        create_mux("GLBOUT.CLK90_1", "GLBOUT.CLK_INT_1", 3, 5, False, "GLBOUT.GLB1", config=True)
        create_mux("GLBOUT.CLK180_1", "GLBOUT.CLK_INT_1", 3, 6, False, "GLBOUT.GLB1", config=True)
        create_mux("GLBOUT.CLK270_1", "GLBOUT.CLK_INT_1", 3, 7, False, "GLBOUT.GLB1", config=True)

        create_mux("GLBOUT.CLK_INT_1", "GLBOUT.CLK_SEL_INT_1", 1, 0, False, "GLBOUT.USR_GLB1", config=True)
        create_mux("GLBOUT.USR_GLB1", "GLBOUT.CLK_SEL_INT_1", 1, 1, False, "GLBOUT.USR_GLB1", config=True)

        create_mux("GLBOUT.CLK_SEL_INT_1", "GLBOUT.GLB1", 1, 1, False, "GLBOUT.GLB1_EN", config=True)

        create_mux("GLBOUT.GLB0", "GLBOUT.FB_INT_1", 2, 0, False, "GLBOUT.FB1", config=True)
        create_mux("GLBOUT.GLB1", "GLBOUT.FB_INT_1", 2, 1, False, "GLBOUT.FB1", config=True)
        create_mux("GLBOUT.GLB2", "GLBOUT.FB_INT_1", 2, 2, False, "GLBOUT.FB1", config=True)
        create_mux("GLBOUT.GLB3", "GLBOUT.FB_INT_1", 2, 3, False, "GLBOUT.FB1", config=True)

        create_mux("GLBOUT.FB_INT_1", "GLBOUT.CLK_FB1", 1, 0, False, "GLBOUT.USR_FB1", config=True)
        create_mux("GLBOUT.USR_FB1", "GLBOUT.CLK_FB1",  1, 1, False, "GLBOUT.USR_FB1", config=True)


        create_mux("GLBOUT.CLK_REF_OUT2", "GLBOUT.CLK_INT_2", 3, 0, False, "GLBOUT.GLB2", config=True)
        create_mux("GLBOUT.CLK180_0", "GLBOUT.CLK_INT_2", 3, 1, False, "GLBOUT.GLB2", config=True)
        create_mux("GLBOUT.CLK180_1", "GLBOUT.CLK_INT_2", 3, 2, False, "GLBOUT.GLB2", config=True)
        create_mux("GLBOUT.CLK180_3", "GLBOUT.CLK_INT_2", 3, 3, False, "GLBOUT.GLB2", config=True)
        create_mux("GLBOUT.CLK0_2", "GLBOUT.CLK_INT_2", 3, 4, False, "GLBOUT.GLB2", config=True)
        create_mux("GLBOUT.CLK90_2", "GLBOUT.CLK_INT_2", 3, 5, False, "GLBOUT.GLB2", config=True)
        create_mux("GLBOUT.CLK180_2", "GLBOUT.CLK_INT_2", 3, 6, False, "GLBOUT.GLB2", config=True)
        create_mux("GLBOUT.CLK270_2", "GLBOUT.CLK_INT_2", 3, 7, False, "GLBOUT.GLB2", config=True)

        create_mux("GLBOUT.CLK_INT_2", "GLBOUT.CLK_SEL_INT_2", 1, 0, False, "GLBOUT.USR_GLB2", config=True)
        create_mux("GLBOUT.USR_GLB2", "GLBOUT.CLK_SEL_INT_2", 1, 1, False, "GLBOUT.USR_GLB2", config=True)

        create_mux("GLBOUT.CLK_SEL_INT_2", "GLBOUT.GLB2", 1, 1, False, "GLBOUT.GLB2_EN", config=True)

        create_mux("GLBOUT.GLB0", "GLBOUT.FB_INT_2", 2, 0, False, "GLBOUT.FB2", config=True)
        create_mux("GLBOUT.GLB1", "GLBOUT.FB_INT_2", 2, 1, False, "GLBOUT.FB2", config=True)
        create_mux("GLBOUT.GLB2", "GLBOUT.FB_INT_2", 2, 2, False, "GLBOUT.FB2", config=True)
        create_mux("GLBOUT.GLB3", "GLBOUT.FB_INT_2", 2, 3, False, "GLBOUT.FB2", config=True)

        create_mux("GLBOUT.FB_INT_2", "GLBOUT.CLK_FB2", 1, 0, False, "GLBOUT.USR_FB2", config=True)
        create_mux("GLBOUT.USR_FB2", "GLBOUT.CLK_FB2",  1, 1, False, "GLBOUT.USR_FB2", config=True)

        create_mux("GLBOUT.CLK_REF_OUT3", "GLBOUT.CLK_INT_3", 3, 0, False, "GLBOUT.GLB3", config=True)
        create_mux("GLBOUT.CLK270_0", "GLBOUT.CLK_INT_3", 3, 1, False, "GLBOUT.GLB3", config=True)
        create_mux("GLBOUT.CLK270_1", "GLBOUT.CLK_INT_3", 3, 2, False, "GLBOUT.GLB3", config=True)
        create_mux("GLBOUT.CLK270_2", "GLBOUT.CLK_INT_3", 3, 3, False, "GLBOUT.GLB3", config=True)
        create_mux("GLBOUT.CLK0_3", "GLBOUT.CLK_INT_3", 3, 4, False, "GLBOUT.GLB3", config=True)
        create_mux("GLBOUT.CLK90_3", "GLBOUT.CLK_INT_3", 3, 5, False, "GLBOUT.GLB3", config=True)
        create_mux("GLBOUT.CLK180_3", "GLBOUT.CLK_INT_3", 3, 6, False, "GLBOUT.GLB3", config=True)
        create_mux("GLBOUT.CLK270_3", "GLBOUT.CLK_INT_3", 3, 7, False, "GLBOUT.GLB3", config=True)

        create_mux("GLBOUT.CLK_INT_3", "GLBOUT.CLK_SEL_INT_3", 1, 0, False, "GLBOUT.USR_GLB3", config=True)
        create_mux("GLBOUT.USR_GLB3", "GLBOUT.CLK_SEL_INT_3", 1, 1, False, "GLBOUT.USR_GLB3", config=True)

        create_mux("GLBOUT.CLK_SEL_INT_3", "GLBOUT.GLB3", 1, 1, False, "GLBOUT.GLB3_EN", config=True)

        create_mux("GLBOUT.GLB0", "GLBOUT.FB_INT_3", 2, 0, False, "GLBOUT.FB3", config=True)
        create_mux("GLBOUT.GLB1", "GLBOUT.FB_INT_3", 2, 1, False, "GLBOUT.FB3", config=True)
        create_mux("GLBOUT.GLB2", "GLBOUT.FB_INT_3", 2, 2, False, "GLBOUT.FB3", config=True)
        create_mux("GLBOUT.GLB3", "GLBOUT.FB_INT_3", 2, 3, False, "GLBOUT.FB3", config=True)

        create_mux("GLBOUT.FB_INT_3", "GLBOUT.CLK_FB3", 1, 0, False, "GLBOUT.USR_FB3", config=True)
        create_mux("GLBOUT.USR_FB3", "GLBOUT.CLK_FB3",  1, 1, False, "GLBOUT.USR_FB3", config=True)

        # PLL

        create_mux("CLKIN.CLK_REF_0", "GLBOUT.CLK_REF_OUT0", 1, 0, False, "PLL0.USR_CLK_OUT", config=True)
        create_mux("CLKIN.CLK_REF_1", "GLBOUT.CLK_REF_OUT1", 1, 0, False, "PLL1.USR_CLK_OUT", config=True)
        create_mux("CLKIN.CLK_REF_2", "GLBOUT.CLK_REF_OUT2", 1, 0, False, "PLL2.USR_CLK_OUT", config=True)
        create_mux("CLKIN.CLK_REF_3", "GLBOUT.CLK_REF_OUT3", 1, 0, False, "PLL3.USR_CLK_OUT", config=True)

        create_mux("PLL0.USR_CLK_REF", "GLBOUT.CLK_REF_OUT0", 1, 1, False, "PLL0.USR_CLK_OUT", config=True)
        create_mux("PLL1.USR_CLK_REF", "GLBOUT.CLK_REF_OUT1", 1, 1, False, "PLL1.USR_CLK_OUT", config=True)
        create_mux("PLL2.USR_CLK_REF", "GLBOUT.CLK_REF_OUT2", 1, 1, False, "PLL2.USR_CLK_OUT", config=True)
        create_mux("PLL3.USR_CLK_REF", "GLBOUT.CLK_REF_OUT3", 1, 1, False, "PLL3.USR_CLK_OUT", config=True)

    return muxes

def get_tile_types(x,y):
    val = list()
    if is_cpe(x,y):
        val.append("CPE")
        val.append("IM")
        if is_outmux(x,y):
            val.append("OM")

    if is_sb_big(x,y):
        val.append("SB_BIG")
    if is_sb_sml(x,y):
        val.append("SB_SML")
    if is_gpio(x,y):
        val.append("GPIO")
    if is_edge_io(x,y):
        val.append("IOES")
    if is_edge_top(x,y):
        val.append("TES")
    if is_edge_bottom(x,y):
        val.append("BES")
    if is_edge_left(x,y):
        val.append("LES")
    if is_edge_right(x,y):
        val.append("RES")
    if is_pll(x,y):
        val.append("PLL")
    if is_serdes(x,y):
        val.append("SERDES")
    if is_cfg_ctrl(x,y):
        val.append("CFG_CTRL")
    if is_ram(x,y):
        val.append("RAM")
    return val

def get_tile_type(x,y):
    val = get_tile_types(x,y)
    if not val:
        val.append("NONE")
    return "_".join(val)

def get_tile_type_list():
    tt = set()
    for y in range(-2, max_row()+1):
        for x in range(-2, max_col()+1):
            tt.add(get_tile_type(x,y))

    return tt

def get_bitstream_tile(x, y):
    # Edge blocks are bit bigger
    if x == -2:
        x += 1
    if x == max_col():
        x -= 1
    if y == -2:
        y += 1
    if y == max_row():
        y -= 1
    return (x + 1) // 2, (y + 1) // 2

def get_tile_info(d,x,y):
    bx, by = get_bitstream_tile(x,y)
    pos = 0
    if is_cpe(x,y):
        pos = ((x+1) % 2) * 2 + ((y+1) % 2) + 1
    if is_edge_top(x,y):
        pos = (x - 1) % 2 + 1
    if is_edge_bottom(x,y):
        pos = (x - 1) % 2 + 1
    if is_edge_left(x,y):
        pos = (y - 1) % 2 + 1
    if is_edge_right(x,y):
        pos = (y - 1) % 2 + 1
    return TileInfo(d, bx, by, pos)

def alt_plane(dir,plane):
    alt = [[5, 6, 7, 8, 1, 2, 3, 4,11,12, 9,10],
           [9,10,11,12, 9,10,11,12,12,11,10, 9]]
    return alt[dir][plane-1]

def prev_plane(p):
    return (p-2) % 12 + 1

def next_plane(p):
    return p % 12 + 1

class Die:
    def __init__(self, name : str, die_x : int, die_y : int):
        self.name = name
        self.die_x = die_x
        self.die_y = die_y
        self.debug_conn = False
        self.offset_x = die_x * num_cols()
        self.offset_y = die_y * num_rows()
        self.io_pad_names = dict()
        self.gpio_to_loc = dict()
        self.conn = dict()
        self.rev_conn = dict()
        for y in range(-2, max_row()+1):
            for x in range(-2, max_col()+1):
                if is_gpio(x,y):
                    io = get_io_name(x,y)
                    if io.bank not in self.io_pad_names:
                        self.io_pad_names[io.bank] = dict()
                    if io.port not in self.io_pad_names[io.bank]:
                        self.io_pad_names[io.bank][io.port] = dict()
                    if io.num not in self.io_pad_names[io.bank][io.port]:
                        self.io_pad_names[io.bank][io.port][io.num] = dict()
                    self.gpio_to_loc[f"GPIO_{io.bank}_{io.port}[{io.num}]"]  = Location(x, y)
                    self.io_pad_names[io.bank][io.port][io.num] = Location(x, y)

    def create_conn(self, src_x,src_y, src, dst_x, dst_y, dst):
        key_val = f"{src_x + self.offset_x}/{src_y + self.offset_y}/{src}"
        key  = Connection(src_x + self.offset_x, src_y + self.offset_y, src)
        item = Connection(dst_x + self.offset_x, dst_y + self.offset_y, dst)
        if key_val not in self.conn:
            self.conn[key_val] = list()
            self.conn[key_val].append(key)
        self.conn[key_val].append(item)
        if "CPE.RAM_I" in dst:
            rev_key_val = f"{dst_x + self.offset_x}/{dst_y + self.offset_y}/{dst}"
            if rev_key_val not in self.rev_conn:
                self.rev_conn[rev_key_val] = list()
                self.rev_conn[rev_key_val].append(item)
            self.rev_conn[rev_key_val].append(key)
        if self.debug_conn:
            print(f"({src_x + self.offset_x},{src_y}) {src} => ({dst_x + self.offset_x},{dst_y + self.offset_y}) {dst}")

    def get_connections_for(self, src_x,src_y, src):
        key_val = f"{src_x + self.offset_x}/{src_y + self.offset_y}/{src}"
        if key_val in self.conn:
            return self.conn[key_val]
        return list()

    def get_connections_to(self, dst_x, dst_y, dst):
        rev_key_val = f"{dst_x + self.offset_x}/{dst_y + self.offset_y}/{dst}"
        if rev_key_val in self.rev_conn:
            return self.rev_conn[rev_key_val]
        return list()

    def create_cpe(self, x,y):
        self.create_conn(x,y,"IM.P01.Y", x,y,"CPE.IN1")
        self.create_conn(x,y,"IM.P02.Y", x,y,"CPE.IN2")
        self.create_conn(x,y,"IM.P03.Y", x,y,"CPE.IN3")
        self.create_conn(x,y,"IM.P04.Y", x,y,"CPE.IN4")
        self.create_conn(x,y,"IM.P05.Y", x,y,"CPE.IN5")
        self.create_conn(x,y,"IM.P06.Y", x,y,"CPE.IN6")
        self.create_conn(x,y,"IM.P07.Y", x,y,"CPE.IN7")
        self.create_conn(x,y,"IM.P08.Y", x,y,"CPE.IN8")
        self.create_conn(x,y,"IM.P09.Y", x,y,"CPE.CLK")
        self.create_conn(x,y,"IM.P10.Y", x,y,"CPE.EN")
        self.create_conn(x,y,"IM.P11.Y", x,y,"CPE.SR")
        if is_cpe(x,y-1):
            self.create_conn(x,y-1,"CPE.COUTY1", x,y,"CPE.CINY1")
            self.create_conn(x,y-1,"CPE.COUTY2", x,y,"CPE.CINY2")
            self.create_conn(x,y-1,"CPE.POUTY1", x,y,"CPE.PINY1")
            self.create_conn(x,y-1,"CPE.POUTY2", x,y,"CPE.PINY2")
        if is_cpe(x-1,y):
            self.create_conn(x-1,y,"CPE.COUTX", x,y,"CPE.CINX")
            self.create_conn(x-1,y,"CPE.POUTX", x,y,"CPE.PINX")

    def create_inmux(self, x,y):
        for p in range(1,13):
            plane = f"{p:02d}"

            # D0 - D3 are from nearby SBs
            offset = 2 if is_sb(x,y) else 1
            self.create_conn(x-offset,y,f"{get_sb_type(x-offset,y)}.P{plane}.Y1", x,y,f"IM.P{plane}.D0")
            self.create_conn(x,y-offset,f"{get_sb_type(x,y-offset)}.P{plane}.Y2", x,y,f"IM.P{plane}.D1")
            self.create_conn(x+offset,y,f"{get_sb_type(x+offset,y)}.P{plane}.Y3", x,y,f"IM.P{plane}.D2")
            self.create_conn(x,y+offset,f"{get_sb_type(x,y+offset)}.P{plane}.Y4", x,y,f"IM.P{plane}.D3")

            # D4 and D5 are from diagonal INMUX
            if is_cpe(x-1,y-1):
                self.create_conn(x-1,y-1,f"IM.P{plane}.Y", x,y,f"IM.P{plane}.D4")
            if is_cpe(x+1,y+1):
                self.create_conn(x+1,y+1,f"IM.P{plane}.Y", x,y,f"IM.P{plane}.D5")

            # D6 and D7 are from alternate planes
            alt = f"{alt_plane(0,p):02d}"
            self.create_conn(x,y,f"IM.P{alt}.Y", x,y,f"IM.P{plane}.D6")
            alt = f"{alt_plane(1,p):02d}"
            self.create_conn(x,y,f"IM.P{alt}.Y", x,y,f"IM.P{plane}.D7")

    def create_sb(self, x,y):
        x_0,y_0 = base_loc(x,y)
        sb_type = get_sb_type(x,y)

        for p in range(1,13):
            plane = f"{p:02d}"
            # Handling input D0
            if is_cpe(x,y):
                # Core section SBs are connected to CPE
                if p < 9:
                    # planes 1..8
                    x_cpe = x_0 + (1 if (p-1) & 2 else 0)
                    y_cpe = y_0 + (1 if (p-1) & 1 else 0)
                    # alternate patterns for lower-left SB(1,1) and upper-right SB(2,2)
                    out = [ 2, 1, 2, 1, 1, 2, 1, 2] if x & 1 else [ 1, 2, 1, 2, 2, 1, 2, 1]
                    self.create_conn(x_cpe,y_cpe,f"CPE.OUT{out[p-1]}", x,y,f"{sb_type}.P{plane}.D0")
                else:
                    # planes 9..12
                    self.create_conn(x,y,f"OM.P{plane}.Y", x,y,f"{sb_type}.P{plane}.D0")
            # Handling GPIO connections is done in create_io
            # Handling inputs D2_* till D7_*
            distances = [2, 4, 8, 12, 16, 20] if is_sb_big(x,y) else [2, 4]
            for i,distance in enumerate(distances):
                for direction in range(4):
                    sb_x, sb_y = x, y
                    match direction:
                        case 0 :
                            sb_x -= distance
                        case 1 :
                            sb_y -= distance
                        case 2 :
                            sb_x += distance
                        case 3 :
                            sb_y += distance
                    if is_sb(sb_x,sb_y):
                        src  = f"{get_sb_type(sb_x,sb_y)}.P{plane}.Y{direction+1}"
                        # Long distance signals are coming from SB_DRIVE
                        if distance > 4:
                            t1x, t1y = (sb_x+16-1) // 8, (sb_y+16-1) // 8
                            t2x, t2y = (x+16-1) // 8, (y+16-1) // 8
                            # depending on distance there are additional inverters
                            # that signal is passing through each 8x8 tile
                            dist = abs(t1x-t2x) + abs(t1y-t2y)
                            if dist % 2 == 1:
                                src = f"SB_DRIVE.P{plane}.D{direction+1}.OUT"
                            else:
                                src = f"SB_DRIVE.P{plane}.D{direction+1}.OUT_NOINV"
                        self.create_conn(sb_x,sb_y, src, x,y,f"{get_sb_type(x,y)}.P{plane}.D{i+2}_{direction+1}")

            if is_sb_big(x,y):
                for direction in range(4):
                    self.create_conn(x,y, f"{get_sb_type(x,y)}.P{plane}.Y{direction+1}", x,y,f"SB_DRIVE.P{plane}.D{direction+1}.IN")

            # Diagonal inputs
            # X12 and X34 on edges are unconnected
            if is_sb(x-1,y-1):
                self.create_conn(x-1,y-1,f"{get_sb_type(x-1,y-1)}.P{plane}.YDIAG", x,y,f"{get_sb_type(x,y)}.P{plane}.X12")
            if is_sb(x+1,y+1):
                self.create_conn(x+1,y+1,f"{get_sb_type(x+1,y+1)}.P{plane}.YDIAG", x,y,f"{get_sb_type(x,y)}.P{plane}.X34")
            self.create_conn(x,y,f"{get_sb_type(x,y)}.P{prev_plane(p):02d}.YDIAG", x,y,f"{get_sb_type(x,y)}.P{plane}.X14")
            self.create_conn(x,y,f"{get_sb_type(x,y)}.P{next_plane(p):02d}.YDIAG", x,y,f"{get_sb_type(x,y)}.P{plane}.X23")

    def create_outmux(self, x,y):
        x_0,y_0 = base_loc(x,y)
        for p in range(9,13):
            plane = f"{p:02d}"
            # alternating patters depending of plane and outmux position
            outputs = [2, 2, 1, 1] if p % 2 == x & 1 else [1, 1, 2, 2]
            self.create_conn(x_0,   y_0,   f"CPE.OUT{outputs[0]}", x,y, f"OM.P{plane}.D0")
            self.create_conn(x_0,   y_0+1, f"CPE.OUT{outputs[1]}", x,y, f"OM.P{plane}.D1")
            self.create_conn(x_0+1, y_0,   f"CPE.OUT{outputs[2]}", x,y, f"OM.P{plane}.D2")
            self.create_conn(x_0+1, y_0+1, f"CPE.OUT{outputs[3]}", x,y, f"OM.P{plane}.D3")

    def create_io(self, x,y):
        cpe_x, cpe_y = gpio_x, gpio_y = sb_x, sb_y = x, y
        alt = False
        if is_edge_left(sb_x,sb_y):
            output = "Y3"
            cpe_x += 3
            if is_sb(sb_x+1,sb_y):
                sb_x += 1
            else:
                sb_x += 2
                gpio_y -= 1
                alt = True
        elif is_edge_right(sb_x,sb_y):
            output = "Y1"
            cpe_x -= 3
            if is_sb(sb_x-1,sb_y):
                sb_x -= 1
                gpio_y -= 1
                alt = True
            else:
                sb_x -= 2
        elif is_edge_bottom(sb_x,sb_y):
            output = "Y4"
            cpe_y += 3
            if is_sb(sb_x,sb_y+1):
                sb_y += 1
            else:
                sb_y += 2
                gpio_x -= 1
                alt = True
        else:
            output = "Y2"
            cpe_y -= 3
            if is_sb(sb_x,sb_y-1):
                sb_y -= 1
                gpio_x -= 1
                alt = True
            else:
                sb_y -= 2

        for p in range(1,13):
            plane = f"{p:02d}"
            self.create_conn(sb_x,sb_y,f"{get_sb_type(sb_x,sb_y)}.P{plane}.{output}", x,y, f"IOES.ALTIN_{plane}")
            self.create_conn(x,y, f"IOES.SB_IN_{plane}", sb_x,sb_y,f"{get_sb_type(sb_x,sb_y)}.P{plane}.D0")
        self.create_conn(gpio_x,gpio_y,"GPIO.IN1", x,y, "IOES.IO_IN1")
        self.create_conn(gpio_x,gpio_y,"GPIO.IN2", x,y, "IOES.IO_IN2")

        if alt:
            self.create_conn(cpe_x, cpe_y, "CPE.RAM_O1", gpio_x,gpio_y,"GPIO.OUT3")
            self.create_conn(cpe_x, cpe_y, "CPE.RAM_O2", gpio_x,gpio_y,"GPIO.OUT4")
        else:
            self.create_conn(cpe_x, cpe_y, "CPE.RAM_O1", gpio_x,gpio_y,"GPIO.OUT1")
            self.create_conn(cpe_x, cpe_y, "CPE.RAM_O2", gpio_x,gpio_y,"GPIO.OUT2")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB0", gpio_x, gpio_y, "GPIO.CLOCK1")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB1", gpio_x, gpio_y, "GPIO.CLOCK2")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB2", gpio_x, gpio_y, "GPIO.CLOCK3")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB3", gpio_x, gpio_y, "GPIO.CLOCK4")

    def create_pll(self):
        # GPIO_W2_A[8]  CLK0
        # GPIO_W2_A[7]  CLK1
        # GPIO_W2_A[6]  CLK2
        # GPIO_W2_A[5]  CLK3
        # SER_CLK       SER_CLK
        # GPIO_S3_B[8]  SPI_CLK
        # GPIO_S3_A[5]  JTAG_CLK
        loc = self.gpio_to_loc["GPIO_W2_A[8]"]
        self.create_conn(loc.x, loc.y, "GPIO.IN1", PLL_X_POS, PLL_Y_POS, "CLKIN.CLK0")
        loc = self.gpio_to_loc["GPIO_W2_A[7]"]
        self.create_conn(loc.x, loc.y, "GPIO.IN1", PLL_X_POS, PLL_Y_POS, "CLKIN.CLK1")
        loc = self.gpio_to_loc["GPIO_W2_A[6]"]
        self.create_conn(loc.x, loc.y, "GPIO.IN1", PLL_X_POS, PLL_Y_POS, "CLKIN.CLK2")
        loc = self.gpio_to_loc["GPIO_W2_A[5]"]
        self.create_conn(loc.x, loc.y, "GPIO.IN1", PLL_X_POS, PLL_Y_POS, "CLKIN.CLK3")

        self.create_conn(1, 128, "CPE.RAM_O1", PLL_X_POS, PLL_Y_POS, "GLBOUT.USR_GLB0")
        self.create_conn(1, 127, "CPE.RAM_O1", PLL_X_POS, PLL_Y_POS, "GLBOUT.USR_GLB1")
        self.create_conn(1, 126, "CPE.RAM_O1", PLL_X_POS, PLL_Y_POS, "GLBOUT.USR_GLB2")
        self.create_conn(1, 125, "CPE.RAM_O1", PLL_X_POS, PLL_Y_POS, "GLBOUT.USR_GLB3")

        self.create_conn(1, 128, "CPE.RAM_O2", PLL_X_POS, PLL_Y_POS, "GLBOUT.USR_FB0")
        self.create_conn(1, 127, "CPE.RAM_O2", PLL_X_POS, PLL_Y_POS, "GLBOUT.USR_FB1")
        self.create_conn(1, 126, "CPE.RAM_O2", PLL_X_POS, PLL_Y_POS, "GLBOUT.USR_FB2")
        self.create_conn(1, 125, "CPE.RAM_O2", PLL_X_POS, PLL_Y_POS, "GLBOUT.USR_FB3")

        self.create_conn(1, 124, "CPE.RAM_O1", PLL_X_POS, PLL_Y_POS, "PLL0.USR_CLK_REF")
        self.create_conn(1, 123, "CPE.RAM_O1", PLL_X_POS, PLL_Y_POS, "PLL1.USR_CLK_REF")
        self.create_conn(1, 122, "CPE.RAM_O1", PLL_X_POS, PLL_Y_POS, "PLL2.USR_CLK_REF")
        self.create_conn(1, 121, "CPE.RAM_O1", PLL_X_POS, PLL_Y_POS, "PLL3.USR_CLK_REF")

        self.create_conn(1, 120, "CPE.RAM_O1", PLL_X_POS, PLL_Y_POS, "PLL0.USR_LOCKED_STDY_RST")
        self.create_conn(1, 119, "CPE.RAM_O1", PLL_X_POS, PLL_Y_POS, "PLL1.USR_LOCKED_STDY_RST")
        self.create_conn(1, 118, "CPE.RAM_O1", PLL_X_POS, PLL_Y_POS, "PLL2.USR_LOCKED_STDY_RST")
        self.create_conn(1, 117, "CPE.RAM_O1", PLL_X_POS, PLL_Y_POS, "PLL3.USR_LOCKED_STDY_RST")

        self.create_conn(1, 116, "CPE.RAM_O1", PLL_X_POS, PLL_Y_POS, "PLL0.USR_SEL_A_B")
        self.create_conn(1, 115, "CPE.RAM_O1", PLL_X_POS, PLL_Y_POS, "PLL1.USR_SEL_A_B")
        self.create_conn(1, 114, "CPE.RAM_O1", PLL_X_POS, PLL_Y_POS, "PLL2.USR_SEL_A_B")
        self.create_conn(1, 113, "CPE.RAM_O1", PLL_X_POS, PLL_Y_POS, "PLL3.USR_SEL_A_B")

        self.create_conn(PLL_X_POS, PLL_Y_POS, "PLL0.USR_PLL_LOCKED", 1, 128, "CPE.RAM_I2")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "PLL1.USR_PLL_LOCKED", 1, 127, "CPE.RAM_I2")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "PLL2.USR_PLL_LOCKED", 1, 126, "CPE.RAM_I2")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "PLL3.USR_PLL_LOCKED", 1, 125, "CPE.RAM_I2")

        self.create_conn(PLL_X_POS, PLL_Y_POS, "PLL0.USR_PLL_LOCKED_STDY", 1, 124, "CPE.RAM_I2")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "PLL1.USR_PLL_LOCKED_STDY", 1, 123, "CPE.RAM_I2")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "PLL2.USR_PLL_LOCKED_STDY", 1, 122, "CPE.RAM_I2")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "PLL3.USR_PLL_LOCKED_STDY", 1, 121, "CPE.RAM_I2")

        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.CLK0_0", 39, 128, "CPE.RAM_I1")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.CLK90_0", 40, 128, "CPE.RAM_I1")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.CLK180_0", 41, 128, "CPE.RAM_I1")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.CLK270_0", 42, 128, "CPE.RAM_I1")

        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.CLK0_1", 43, 128, "CPE.RAM_I1")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.CLK90_1", 44, 128, "CPE.RAM_I1")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.CLK180_1", 45, 128, "CPE.RAM_I1")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.CLK270_1", 46, 128, "CPE.RAM_I1")

        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.CLK0_2", 47, 128, "CPE.RAM_I1")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.CLK90_2", 48, 128, "CPE.RAM_I1")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.CLK180_2", 49, 128, "CPE.RAM_I1")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.CLK270_2", 50, 128, "CPE.RAM_I1")

        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.CLK0_3", 51, 128, "CPE.RAM_I1")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.CLK90_3", 52, 128, "CPE.RAM_I1")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.CLK180_3", 53, 128, "CPE.RAM_I1")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.CLK270_3", 54, 128, "CPE.RAM_I1")


    def global_mesh(self):
        def global_mesh_conn(x,y,inp):
            for p in range(1,13):
                plane = f"{p:02d}"
                if is_sb_big(x,y):
                    # Clock#1: p1, p5,p9
                    # Clock#2: p2, p6,p10
                    # Clock#3: p3, p7,p11
                    # Clock#4: p4, p8,p12
                    self.create_conn(PLL_X_POS, PLL_Y_POS, f"GLBOUT.GLB{(p-1) & 3}", x,y,f"SB_BIG.P{plane}.{inp}")

        # Connecting Global Mesh signals to Switch Boxes
        # Left edge
        for y in range(0,130+1):
            x = 2 - (y % 4)
            global_mesh_conn(x,y,"D7_1")
        global_mesh_conn(-1,-1,"D7_1")

        # Bottom edge
        for x in range(0,162+1):
            y = 2 - (x % 4)
            global_mesh_conn(x,y,"D7_2")
        global_mesh_conn(-1,-1,"D7_2")

        # Right edge
        for y in range(0,130+1):
            x = 2 - (y % 4) + 160
            global_mesh_conn(x,y,"D7_3")
        global_mesh_conn(159,-1,"D7_3")

        # Top edge
        for x in range(0,162+1):
            y = 2 - (x % 4) + 128
            global_mesh_conn(x,y,"D7_4")
        global_mesh_conn(-1,127,"D7_4")

        # Connecting Global Mesh signals to CPEs
        #for m in range (0,3+1):
        #    for n in range (0,7+1):
        #        x0 = 33 + m * 32
        #        y0 = 1 + n * 16
        #        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB0", x0 - 3, y0 + 10 , "CPE.RAM_I1")
        #        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB1", x0 - 3, y0 + 11 , "CPE.RAM_I1")
        #        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB2", x0 - 3, y0 + 12 , "CPE.RAM_I1")
        #        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB3", x0 - 3, y0 + 13 , "CPE.RAM_I1")
#
        #        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB0", x0 + 2, y0 + 10 , "CPE.RAM_I2")
        #        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB1", x0 + 2, y0 + 11 , "CPE.RAM_I2")
        #        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB2", x0 + 2, y0 + 12 , "CPE.RAM_I2")
        #        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB3", x0 + 2, y0 + 13 , "CPE.RAM_I2")

    def edge_select(self):
        # Left edge
        for y in range(1,128+1):
            self.create_conn(-2, y, "LES.CPE_CINX", 1, y ,"CPE.CINX")
            self.create_conn(-2, y, "LES.CPE_PINX", 1, y ,"CPE.PINX")

            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB0", -2, y, "LES.CLOCK0")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB1", -2, y, "LES.CLOCK1")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB2", -2, y, "LES.CLOCK2")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB3", -2, y, "LES.CLOCK3")

            for p in range(1,9):
                plane = f"{p:02d}"
                sb_x = -1 if y % 2==1 else 0
                self.create_conn(sb_x, y, f"{get_sb_type(sb_x,y)}.P{plane}.Y3", -2, y, f"LES.SB_Y3.P{p}")

        # Bottom edge
        for x in range(1,160+1):
            self.create_conn(x, -2, "BES.CPE_CINY1", x, 1 ,"CPE.CINY1")
            self.create_conn(x, -2, "BES.CPE_PINY1", x, 1 ,"CPE.PINY1")
            self.create_conn(x, -2, "BES.CPE_CINY2", x, 1 ,"CPE.CINY2")
            self.create_conn(x, -2, "BES.CPE_PINY2", x, 1 ,"CPE.PINY2")
            if x>1:
                self.create_conn(x-1, -2, "BES.CPE_CINY1", x, -2 ,"BES.P_CINY1")
                self.create_conn(x-1, -2, "BES.CPE_PINY1", x, -2 ,"BES.P_PINY1")
                self.create_conn(x-1, -2, "BES.CPE_CINY2", x, -2 ,"BES.P_CINY2")
                self.create_conn(x-1, -2, "BES.CPE_PINY2", x, -2 ,"BES.P_PINY2")

            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB0", x, -2, "BES.CLOCK0")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB1", x, -2, "BES.CLOCK1")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB2", x, -2, "BES.CLOCK2")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB3", x, -2, "BES.CLOCK3")

            for p in range(1,9):
                plane = f"{p:02d}"
                sb_y = -1 if x % 2==1 else 0
                self.create_conn(x, sb_y, f"{get_sb_type(x,sb_y)}.P{plane}.Y4", x, -2, f"BES.SB_Y4.P{p}")

        # Right edge
        for y in range(1,128+1):
            self.create_conn(160, y, "CPE.RAM_O1", 163, y ,"RES.CPE_RAM_O1")
            self.create_conn(160, y, "CPE.RAM_O2", 163, y ,"RES.CPE_RAM_O2")
            self.create_conn(160, y, "CPE.COUTX", 163, y ,"RES.CPE_COUTX")
            self.create_conn(160, y, "CPE.POUTX", 163, y ,"RES.CPE_POUTX")

            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB0", 163, y, "RES.CLOCK0")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB1", 163, y, "RES.CLOCK1")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB2", 163, y, "RES.CLOCK2")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB3", 163, y, "RES.CLOCK3")

            for p in range(1,9):
                plane = f"{p:02d}"
                sb_x = 161 if y % 2==1 else 162
                self.create_conn(sb_x, y, f"{get_sb_type(sb_x,y)}.P{plane}.Y1", 163, y, f"RES.SB_Y1.P{p}")

        # Top edge
        for x in range(28,160+1):
            self.create_conn(x, 128 ,"CPE.RAM_O1", x, 131, "TES.CPE_RAM_O1")
            self.create_conn(x, 128 ,"CPE.RAM_O2", x, 131, "TES.CPE_RAM_O2")
            self.create_conn(x, 128 ,"CPE.COUTY1", x, 131, "TES.CPE_COUTY1")
            self.create_conn(x, 128 ,"CPE.POUTY1", x, 131, "TES.CPE_POUTY1")
            self.create_conn(x, 128 ,"CPE.COUTY2", x, 131, "TES.CPE_COUTY2")
            self.create_conn(x, 128 ,"CPE.POUTY2", x, 131, "TES.CPE_POUTY2")

            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB0", x, 131, "TES.CLOCK0")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB1", x, 131, "TES.CLOCK1")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB2", x, 131, "TES.CLOCK2")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB3", x, 131, "TES.CLOCK3")

            for p in range(1,9):
                plane = f"{p:02d}"
                sb_y = 129 if x % 2==1 else 130
                self.create_conn(x, sb_y, f"{get_sb_type(x,sb_y)}.P{plane}.Y2", x, 131, f"TES.SB_Y2.P{p}")

    def connect_ddr_i(self, x, y, out, bank):
        for port in ['A','B']:
            for num in range(0,9):
                loc = self.io_pad_names[bank][port][num]
                self.create_conn(x, y , f"CPE.RAM_O{out}", loc.x, loc.y, "GPIO.DDR")

    def misc_connections(self):
        self.create_conn(1, 16, "CPE.RAM_O1", CTRL_X_POS, CTRL_Y_POS, "CFG_CTRL.DATA[7]")
        self.create_conn(1, 15, "CPE.RAM_O1", CTRL_X_POS, CTRL_Y_POS, "CFG_CTRL.DATA[6]")
        self.create_conn(1, 14, "CPE.RAM_O1", CTRL_X_POS, CTRL_Y_POS, "CFG_CTRL.DATA[5]")
        self.create_conn(1, 13, "CPE.RAM_O1", CTRL_X_POS, CTRL_Y_POS, "CFG_CTRL.DATA[4]")
        self.create_conn(1, 12, "CPE.RAM_O1", CTRL_X_POS, CTRL_Y_POS, "CFG_CTRL.DATA[3]")
        self.create_conn(1, 11, "CPE.RAM_O1", CTRL_X_POS, CTRL_Y_POS, "CFG_CTRL.DATA[2]")
        self.create_conn(1, 10, "CPE.RAM_O1", CTRL_X_POS, CTRL_Y_POS, "CFG_CTRL.DATA[1]")
        self.create_conn(1,  9, "CPE.RAM_O1", CTRL_X_POS, CTRL_Y_POS, "CFG_CTRL.DATA[0]")

        self.create_conn(1,  6, "CPE.RAM_O1", CTRL_X_POS, CTRL_Y_POS, "CFG_CTRL.CLK")
        self.create_conn(1,  7, "CPE.RAM_O1", CTRL_X_POS, CTRL_Y_POS, "CFG_CTRL.EN")
        self.create_conn(1,  8, "CPE.RAM_O1", CTRL_X_POS, CTRL_Y_POS, "CFG_CTRL.VALID")

        self.create_conn(1,  5, "CPE.RAM_O1", CTRL_X_POS, CTRL_Y_POS, "CFG_CTRL.RECFG")

        self.create_conn(CTRL_X_POS, CTRL_Y_POS ,"USR_RSTN.USR_RSTN", 1, 66, "CPE.RAM_I2")

        self.connect_ddr_i(97,128,1,'N1')
        self.connect_ddr_i(97,128,2,'N2')
        self.connect_ddr_i(160,65,1,'E1')
        self.connect_ddr_i(160,65,2,'E2')
        self.connect_ddr_i(1,65,1,'W1')
        self.connect_ddr_i(1,65,2,'W2')
        self.connect_ddr_i(97,1,1,'S1')
        self.connect_ddr_i(97,1,2,'S2')
        self.connect_ddr_i(49,1,1,'S3')

    def create_serdes(self, x, y):
        self.create_conn(x+6,y+6,"CPE.RAM_O1", x,y,"SERDES.TX_DETECT_RX_I")
        self.create_conn(x+6,y+5,"CPE.RAM_O2", x,y,"SERDES.PLL_RESET_I")
        self.create_conn(x+6,y+5,"CPE.RAM_O1", x,y,"SERDES.REGFILE_CLK_I")
        self.create_conn(x+6,y+4,"CPE.RAM_O2", x,y,"SERDES.TX_CLK_I")
        self.create_conn(x+6,y+4,"CPE.RAM_O1", x,y,"SERDES.RX_CLK_I")
        self.create_conn(x+6,y+3,"CPE.RAM_O2", x,y,"SERDES.REGFILE_WE_I")
        self.create_conn(x+6,y+3,"CPE.RAM_O1", x,y,"SERDES.REGFILE_EN_I")
        self.create_conn(x+6,y+2,"CPE.RAM_O2", x,y,"SERDES.TX_RESET_I")
        self.create_conn(x+6,y+2,"CPE.RAM_O1", x,y,"SERDES.TX_PCS_RESET_I")
        self.create_conn(x+6,y+1,"CPE.RAM_O2", x,y,"SERDES.TX_PMA_RESET_I")
        self.create_conn(x+6,y+1,"CPE.RAM_O1", x,y,"SERDES.TX_PRBS_FORCE_ERR_I")
        self.create_conn(x+6,y+0,"CPE.RAM_O2", x,y,"SERDES.TX_POLARITY_I")
        self.create_conn(x+6,y+0,"CPE.RAM_O1", x,y,"SERDES.TX_8B10B_EN_I")
        self.create_conn(x+7,y+6,"CPE.RAM_O2", x,y,"SERDES.RX_RESET_I")
        self.create_conn(x+7,y+6,"CPE.RAM_O1", x,y,"SERDES.RX_PMA_RESET_I")
        self.create_conn(x+7,y+5,"CPE.RAM_O2", x,y,"SERDES.RX_EQA_RESET_I")
        self.create_conn(x+7,y+5,"CPE.RAM_O1", x,y,"SERDES.RX_CDR_RESET_I")
        self.create_conn(x+7,y+4,"CPE.RAM_O2", x,y,"SERDES.RX_PCS_RESET_I")
        self.create_conn(x+7,y+4,"CPE.RAM_O1", x,y,"SERDES.RX_BUF_RESET_I")
        self.create_conn(x+7,y+3,"CPE.RAM_O2", x,y,"SERDES.RX_PRBS_CNT_RESET_I")
        self.create_conn(x+7,y+3,"CPE.RAM_O1", x,y,"SERDES.RX_EN_EI_DETECTOR_I")
        self.create_conn(x+7,y+2,"CPE.RAM_O2", x,y,"SERDES.RX_COMMA_DETECT_EN_I")
        self.create_conn(x+7,y+2,"CPE.RAM_O1", x,y,"SERDES.RX_SLIDE_I")
        self.create_conn(x+7,y+1,"CPE.RAM_O2", x,y,"SERDES.RX_POLARITY_I")
        self.create_conn(x+7,y+1,"CPE.RAM_O1", x,y,"SERDES.RX_8B10B_EN_I")
        self.create_conn(x+7,y+0,"CPE.RAM_O2", x,y,"SERDES.RX_MCOMMA_ALIGN_I")
        self.create_conn(x+7,y+0,"CPE.RAM_O1", x,y,"SERDES.RX_PCOMMA_ALIGN_I")
        self.create_conn(x,y,"SERDES.RX_NOT_IN_TABLE_O[7]", x+8,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_NOT_IN_TABLE_O[6]", x+8,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_NOT_IN_TABLE_O[5]", x+9,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_NOT_IN_TABLE_O[4]", x+9,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_NOT_IN_TABLE_O[3]", x+10,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_NOT_IN_TABLE_O[2]", x+10,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_NOT_IN_TABLE_O[1]", x+11,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_NOT_IN_TABLE_O[0]", x+11,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_CHAR_IS_COMMA_O[7]", x+12,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_CHAR_IS_COMMA_O[6]", x+12,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_CHAR_IS_COMMA_O[5]", x+13,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_CHAR_IS_COMMA_O[4]", x+13,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_CHAR_IS_COMMA_O[3]", x+14,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_CHAR_IS_COMMA_O[2]", x+14,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_CHAR_IS_COMMA_O[1]", x+15,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_CHAR_IS_COMMA_O[0]", x+15,y+7,"CPE.RAM_I2")
        self.create_conn(x+8,y+6,"CPE.RAM_O1", x,y,"SERDES.REGFILE_ADDR_I[7]")
        self.create_conn(x+8,y+6,"CPE.RAM_O2", x,y,"SERDES.REGFILE_ADDR_I[6]")
        self.create_conn(x+9,y+6,"CPE.RAM_O1", x,y,"SERDES.REGFILE_ADDR_I[5]")
        self.create_conn(x+9,y+6,"CPE.RAM_O2", x,y,"SERDES.REGFILE_ADDR_I[4]")
        self.create_conn(x+10,y+6,"CPE.RAM_O1", x,y,"SERDES.REGFILE_ADDR_I[3]")
        self.create_conn(x+10,y+6,"CPE.RAM_O2", x,y,"SERDES.REGFILE_ADDR_I[2]")
        self.create_conn(x+11,y+6,"CPE.RAM_O1", x,y,"SERDES.REGFILE_ADDR_I[1]")
        self.create_conn(x+11,y+6,"CPE.RAM_O2", x,y,"SERDES.REGFILE_ADDR_I[0]")
        self.create_conn(x+12,y+6,"CPE.RAM_O1", x,y,"SERDES.TX_CHAR_IS_K_I[7]")
        self.create_conn(x+12,y+6,"CPE.RAM_O2", x,y,"SERDES.TX_CHAR_IS_K_I[6]")
        self.create_conn(x+13,y+6,"CPE.RAM_O1", x,y,"SERDES.TX_CHAR_IS_K_I[5]")
        self.create_conn(x+13,y+6,"CPE.RAM_O2", x,y,"SERDES.TX_CHAR_IS_K_I[4]")
        self.create_conn(x+14,y+6,"CPE.RAM_O1", x,y,"SERDES.TX_CHAR_IS_K_I[3]")
        self.create_conn(x+14,y+6,"CPE.RAM_O2", x,y,"SERDES.TX_CHAR_IS_K_I[2]")
        self.create_conn(x+15,y+6,"CPE.RAM_O1", x,y,"SERDES.TX_CHAR_IS_K_I[1]")
        self.create_conn(x+15,y+6,"CPE.RAM_O2", x,y,"SERDES.TX_CHAR_IS_K_I[0]")
        self.create_conn(x+8,y+5,"CPE.RAM_O1", x,y,"SERDES.TX_8B10B_BYPASS_I[7]")
        self.create_conn(x+8,y+5,"CPE.RAM_O2", x,y,"SERDES.TX_8B10B_BYPASS_I[6]")
        self.create_conn(x+9,y+5,"CPE.RAM_O1", x,y,"SERDES.TX_8B10B_BYPASS_I[5]")
        self.create_conn(x+9,y+5,"CPE.RAM_O2", x,y,"SERDES.TX_8B10B_BYPASS_I[4]")
        self.create_conn(x+10,y+5,"CPE.RAM_O1", x,y,"SERDES.TX_8B10B_BYPASS_I[3]")
        self.create_conn(x+10,y+5,"CPE.RAM_O2", x,y,"SERDES.TX_8B10B_BYPASS_I[2]")
        self.create_conn(x+11,y+5,"CPE.RAM_O1", x,y,"SERDES.TX_8B10B_BYPASS_I[1]")
        self.create_conn(x+11,y+5,"CPE.RAM_O2", x,y,"SERDES.TX_8B10B_BYPASS_I[0]")
        self.create_conn(x+12,y+5,"CPE.RAM_O1", x,y,"SERDES.RX_8B10B_BYPASS_I[7]")
        self.create_conn(x+12,y+5,"CPE.RAM_O2", x,y,"SERDES.RX_8B10B_BYPASS_I[6]")
        self.create_conn(x+13,y+5,"CPE.RAM_O1", x,y,"SERDES.RX_8B10B_BYPASS_I[5]")
        self.create_conn(x+13,y+5,"CPE.RAM_O2", x,y,"SERDES.RX_8B10B_BYPASS_I[4]")
        self.create_conn(x+14,y+5,"CPE.RAM_O1", x,y,"SERDES.RX_8B10B_BYPASS_I[3]")
        self.create_conn(x+14,y+5,"CPE.RAM_O2", x,y,"SERDES.RX_8B10B_BYPASS_I[2]")
        self.create_conn(x+15,y+5,"CPE.RAM_O1", x,y,"SERDES.RX_8B10B_BYPASS_I[1]")
        self.create_conn(x+15,y+5,"CPE.RAM_O2", x,y,"SERDES.RX_8B10B_BYPASS_I[0]")
        self.create_conn(x+8,y+4,"CPE.RAM_O1", x,y,"SERDES.TX_CHAR_DISPMODE_I[7]")
        self.create_conn(x+8,y+4,"CPE.RAM_O2", x,y,"SERDES.TX_CHAR_DISPMODE_I[6]")
        self.create_conn(x+9,y+4,"CPE.RAM_O1", x,y,"SERDES.TX_CHAR_DISPMODE_I[5]")
        self.create_conn(x+9,y+4,"CPE.RAM_O2", x,y,"SERDES.TX_CHAR_DISPMODE_I[4]")
        self.create_conn(x+10,y+4,"CPE.RAM_O1", x,y,"SERDES.TX_CHAR_DISPMODE_I[3]")
        self.create_conn(x+10,y+4,"CPE.RAM_O2", x,y,"SERDES.TX_CHAR_DISPMODE_I[2]")
        self.create_conn(x+11,y+4,"CPE.RAM_O1", x,y,"SERDES.TX_CHAR_DISPMODE_I[1]")
        self.create_conn(x+11,y+4,"CPE.RAM_O2", x,y,"SERDES.TX_CHAR_DISPMODE_I[0]")
        self.create_conn(x+12,y+4,"CPE.RAM_O1", x,y,"SERDES.TX_CHAR_DISPVAL_I[7]")
        self.create_conn(x+12,y+4,"CPE.RAM_O2", x,y,"SERDES.TX_CHAR_DISPVAL_I[6]")
        self.create_conn(x+13,y+4,"CPE.RAM_O1", x,y,"SERDES.TX_CHAR_DISPVAL_I[5]")
        self.create_conn(x+13,y+4,"CPE.RAM_O2", x,y,"SERDES.TX_CHAR_DISPVAL_I[4]")
        self.create_conn(x+14,y+4,"CPE.RAM_O1", x,y,"SERDES.TX_CHAR_DISPVAL_I[3]")
        self.create_conn(x+14,y+4,"CPE.RAM_O2", x,y,"SERDES.TX_CHAR_DISPVAL_I[2]")
        self.create_conn(x+15,y+4,"CPE.RAM_O1", x,y,"SERDES.TX_CHAR_DISPVAL_I[1]")
        self.create_conn(x+15,y+4,"CPE.RAM_O2", x,y,"SERDES.TX_CHAR_DISPVAL_I[0]")
        self.create_conn(x+8,y+3,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[63]")
        self.create_conn(x+8,y+3,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[62]")
        self.create_conn(x+9,y+3,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[61]")
        self.create_conn(x+9,y+3,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[60]")
        self.create_conn(x+10,y+3,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[59]")
        self.create_conn(x+10,y+3,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[58]")
        self.create_conn(x+11,y+3,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[57]")
        self.create_conn(x+11,y+3,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[56]")
        self.create_conn(x+12,y+3,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[55]")
        self.create_conn(x+12,y+3,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[54]")
        self.create_conn(x+13,y+3,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[53]")
        self.create_conn(x+13,y+3,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[52]")
        self.create_conn(x+14,y+3,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[51]")
        self.create_conn(x+14,y+3,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[50]")
        self.create_conn(x+15,y+3,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[49]")
        self.create_conn(x+15,y+3,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[48]")
        self.create_conn(x+8,y+2,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[47]")
        self.create_conn(x+8,y+2,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[46]")
        self.create_conn(x+9,y+2,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[45]")
        self.create_conn(x+9,y+2,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[44]")
        self.create_conn(x+10,y+2,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[43]")
        self.create_conn(x+10,y+2,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[42]")
        self.create_conn(x+11,y+2,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[41]")
        self.create_conn(x+11,y+2,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[40]")
        self.create_conn(x+12,y+2,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[39]")
        self.create_conn(x+12,y+2,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[38]")
        self.create_conn(x+13,y+2,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[37]")
        self.create_conn(x+13,y+2,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[36]")
        self.create_conn(x+14,y+2,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[35]")
        self.create_conn(x+14,y+2,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[34]")
        self.create_conn(x+15,y+2,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[33]")
        self.create_conn(x+15,y+2,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[32]")
        self.create_conn(x+8,y+1,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[31]")
        self.create_conn(x+8,y+1,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[30]")
        self.create_conn(x+9,y+1,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[29]")
        self.create_conn(x+9,y+1,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[28]")
        self.create_conn(x+10,y+1,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[27]")
        self.create_conn(x+10,y+1,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[26]")
        self.create_conn(x+11,y+1,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[25]")
        self.create_conn(x+11,y+1,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[24]")
        self.create_conn(x+12,y+1,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[23]")
        self.create_conn(x+12,y+1,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[22]")
        self.create_conn(x+13,y+1,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[21]")
        self.create_conn(x+13,y+1,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[20]")
        self.create_conn(x+14,y+1,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[19]")
        self.create_conn(x+14,y+1,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[18]")
        self.create_conn(x+15,y+1,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[17]")
        self.create_conn(x+15,y+1,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[16]")
        self.create_conn(x+8,y+0,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[15]")
        self.create_conn(x+8,y+0,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[14]")
        self.create_conn(x+9,y+0,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[13]")
        self.create_conn(x+9,y+0,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[12]")
        self.create_conn(x+10,y+0,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[11]")
        self.create_conn(x+10,y+0,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[10]")
        self.create_conn(x+11,y+0,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[9]")
        self.create_conn(x+11,y+0,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[8]")
        self.create_conn(x+12,y+0,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[7]")
        self.create_conn(x+12,y+0,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[6]")
        self.create_conn(x+13,y+0,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[5]")
        self.create_conn(x+13,y+0,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[4]")
        self.create_conn(x+14,y+0,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[3]")
        self.create_conn(x+14,y+0,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[2]")
        self.create_conn(x+15,y+0,"CPE.RAM_O1", x,y,"SERDES.TX_DATA_I[1]")
        self.create_conn(x+15,y+0,"CPE.RAM_O2", x,y,"SERDES.TX_DATA_I[0]")
        self.create_conn(x,y,"SERDES.REGFILE_DO_O[15]", x+16,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.REGFILE_DO_O[14]", x+16,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.REGFILE_DO_O[13]", x+17,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.REGFILE_DO_O[12]", x+17,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.REGFILE_DO_O[11]", x+18,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.REGFILE_DO_O[10]", x+18,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.REGFILE_DO_O[9]", x+19,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.REGFILE_DO_O[8]", x+19,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.REGFILE_DO_O[7]", x+20,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.REGFILE_DO_O[6]", x+20,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.REGFILE_DO_O[5]", x+21,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.REGFILE_DO_O[4]", x+21,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.REGFILE_DO_O[3]", x+22,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.REGFILE_DO_O[2]", x+22,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.REGFILE_DO_O[1]", x+23,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.REGFILE_DO_O[0]", x+23,y+7,"CPE.RAM_I2")
        self.create_conn(x+16,y+6,"CPE.RAM_O1", x,y,"SERDES.REGFILE_DI_I[15]")
        self.create_conn(x+16,y+6,"CPE.RAM_O2", x,y,"SERDES.REGFILE_DI_I[14]")
        self.create_conn(x+17,y+6,"CPE.RAM_O1", x,y,"SERDES.REGFILE_DI_I[13]")
        self.create_conn(x+17,y+6,"CPE.RAM_O2", x,y,"SERDES.REGFILE_DI_I[12]")
        self.create_conn(x+18,y+6,"CPE.RAM_O1", x,y,"SERDES.REGFILE_DI_I[11]")
        self.create_conn(x+18,y+6,"CPE.RAM_O2", x,y,"SERDES.REGFILE_DI_I[10]")
        self.create_conn(x+19,y+6,"CPE.RAM_O1", x,y,"SERDES.REGFILE_DI_I[9]")
        self.create_conn(x+19,y+6,"CPE.RAM_O2", x,y,"SERDES.REGFILE_DI_I[8]")
        self.create_conn(x+20,y+6,"CPE.RAM_O1", x,y,"SERDES.REGFILE_DI_I[7]")
        self.create_conn(x+20,y+6,"CPE.RAM_O2", x,y,"SERDES.REGFILE_DI_I[6]")
        self.create_conn(x+21,y+6,"CPE.RAM_O1", x,y,"SERDES.REGFILE_DI_I[5]")
        self.create_conn(x+21,y+6,"CPE.RAM_O2", x,y,"SERDES.REGFILE_DI_I[4]")
        self.create_conn(x+22,y+6,"CPE.RAM_O1", x,y,"SERDES.REGFILE_DI_I[3]")
        self.create_conn(x+22,y+6,"CPE.RAM_O2", x,y,"SERDES.REGFILE_DI_I[2]")
        self.create_conn(x+23,y+6,"CPE.RAM_O1", x,y,"SERDES.REGFILE_DI_I[1]")
        self.create_conn(x+23,y+6,"CPE.RAM_O2", x,y,"SERDES.REGFILE_DI_I[0]")
        self.create_conn(x+16,y+5,"CPE.RAM_O1", x,y,"SERDES.REGFILE_MASK_I[15]")
        self.create_conn(x+16,y+5,"CPE.RAM_O2", x,y,"SERDES.REGFILE_MASK_I[14]")
        self.create_conn(x+17,y+5,"CPE.RAM_O1", x,y,"SERDES.REGFILE_MASK_I[13]")
        self.create_conn(x+17,y+5,"CPE.RAM_O2", x,y,"SERDES.REGFILE_MASK_I[12]")
        self.create_conn(x+18,y+5,"CPE.RAM_O1", x,y,"SERDES.REGFILE_MASK_I[11]")
        self.create_conn(x+18,y+5,"CPE.RAM_O2", x,y,"SERDES.REGFILE_MASK_I[10]")
        self.create_conn(x+19,y+5,"CPE.RAM_O1", x,y,"SERDES.REGFILE_MASK_I[9]")
        self.create_conn(x+19,y+5,"CPE.RAM_O2", x,y,"SERDES.REGFILE_MASK_I[8]")
        self.create_conn(x+20,y+5,"CPE.RAM_O1", x,y,"SERDES.REGFILE_MASK_I[7]")
        self.create_conn(x+20,y+5,"CPE.RAM_O2", x,y,"SERDES.REGFILE_MASK_I[6]")
        self.create_conn(x+21,y+5,"CPE.RAM_O1", x,y,"SERDES.REGFILE_MASK_I[5]")
        self.create_conn(x+21,y+5,"CPE.RAM_O2", x,y,"SERDES.REGFILE_MASK_I[4]")
        self.create_conn(x+22,y+5,"CPE.RAM_O1", x,y,"SERDES.REGFILE_MASK_I[3]")
        self.create_conn(x+22,y+5,"CPE.RAM_O2", x,y,"SERDES.REGFILE_MASK_I[2]")
        self.create_conn(x+23,y+5,"CPE.RAM_O1", x,y,"SERDES.REGFILE_MASK_I[1]")
        self.create_conn(x+23,y+5,"CPE.RAM_O2", x,y,"SERDES.REGFILE_MASK_I[0]")
        self.create_conn(x,y,"SERDES.RX_CHAR_IS_K_O[7]", x+16,y+4,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_CHAR_IS_K_O[6]", x+16,y+4,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_CHAR_IS_K_O[5]", x+17,y+4,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_CHAR_IS_K_O[4]", x+17,y+4,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_CHAR_IS_K_O[3]", x+18,y+4,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_CHAR_IS_K_O[2]", x+18,y+4,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_CHAR_IS_K_O[1]", x+19,y+4,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_CHAR_IS_K_O[0]", x+19,y+4,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DISP_ERR_O[7]", x+20,y+4,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DISP_ERR_O[6]", x+20,y+4,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DISP_ERR_O[5]", x+21,y+4,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DISP_ERR_O[4]", x+21,y+4,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DISP_ERR_O[3]", x+22,y+4,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DISP_ERR_O[2]", x+22,y+4,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DISP_ERR_O[1]", x+23,y+4,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DISP_ERR_O[0]", x+23,y+4,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[63]", x+16,y+3,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[62]", x+16,y+3,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[61]", x+17,y+3,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[60]", x+17,y+3,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[59]", x+18,y+3,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[58]", x+18,y+3,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[57]", x+19,y+3,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[56]", x+19,y+3,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[55]", x+20,y+3,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[54]", x+20,y+3,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[53]", x+21,y+3,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[52]", x+21,y+3,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[51]", x+22,y+3,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[50]", x+22,y+3,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[49]", x+23,y+3,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[48]", x+23,y+3,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[47]", x+16,y+2,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[46]", x+16,y+2,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[45]", x+17,y+2,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[44]", x+17,y+2,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[43]", x+18,y+2,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[42]", x+18,y+2,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[41]", x+19,y+2,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[40]", x+19,y+2,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[39]", x+20,y+2,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[38]", x+20,y+2,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[37]", x+21,y+2,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[36]", x+21,y+2,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[35]", x+22,y+2,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[34]", x+22,y+2,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[33]", x+23,y+2,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[32]", x+23,y+2,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[31]", x+16,y+1,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[30]", x+16,y+1,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[29]", x+17,y+1,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[28]", x+17,y+1,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[27]", x+18,y+1,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[26]", x+18,y+1,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[25]", x+19,y+1,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[24]", x+19,y+1,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[23]", x+20,y+1,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[22]", x+20,y+1,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[21]", x+21,y+1,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[20]", x+21,y+1,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[19]", x+22,y+1,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[18]", x+22,y+1,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[17]", x+23,y+1,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[16]", x+23,y+1,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[15]", x+16,y+0,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[14]", x+16,y+0,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[13]", x+17,y+0,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[12]", x+17,y+0,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[11]", x+18,y+0,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[10]", x+18,y+0,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[9]", x+19,y+0,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[8]", x+19,y+0,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[7]", x+20,y+0,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[6]", x+20,y+0,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[5]", x+21,y+0,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[4]", x+21,y+0,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[3]", x+22,y+0,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[2]", x+22,y+0,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_DATA_O[1]", x+23,y+0,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_DATA_O[0]", x+23,y+0,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.TX_DETECT_RX_DONE_O", x+24,y+6,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.TX_DETECT_RX_PRESENT_O", x+24,y+6,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_CLK_O", x+24,y+5,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.PLL_CLK_O", x+24,y+5,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.TX_BUF_ERR_O", x+24,y+4,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.TX_RESET_DONE_O", x+24,y+4,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.REGFILE_RDY_O", x+24,y+3,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_PRBS_ERR_O", x+24,y+3,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_BUF_ERR_O", x+24,y+2,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_BYTE_IS_ALIGNED_O", x+24,y+2,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_BYTE_REALIGN_O", x+24,y+1,"CPE.RAM_I2")
        self.create_conn(x,y,"SERDES.RX_RESET_DONE_O", x+24,y+1,"CPE.RAM_I1")
        self.create_conn(x,y,"SERDES.RX_EI_EN_O", x+24,y+0,"CPE.RAM_I2")
        self.create_conn(x+25,y+5,"CPE.RAM_O1", x,y,"SERDES.LOOPBACK_I[2]")
        self.create_conn(x+25,y+5,"CPE.RAM_O2", x,y,"SERDES.LOOPBACK_I[1]")
        self.create_conn(x+25,y+4,"CPE.RAM_O2", x,y,"SERDES.LOOPBACK_I[0]")
        self.create_conn(x+25,y+3,"CPE.RAM_O1", x,y,"SERDES.TX_PRBS_SEL_I[2]")
        self.create_conn(x+25,y+3,"CPE.RAM_O2", x,y,"SERDES.TX_PRBS_SEL_I[1]")
        self.create_conn(x+25,y+2,"CPE.RAM_O2", x,y,"SERDES.TX_PRBS_SEL_I[0]")
        self.create_conn(x+25,y+1,"CPE.RAM_O1", x,y,"SERDES.RX_PRBS_SEL_I[2]")
        self.create_conn(x+25,y+1,"CPE.RAM_O2", x,y,"SERDES.RX_PRBS_SEL_I[1]")
        self.create_conn(x+25,y+0,"CPE.RAM_O2", x,y,"SERDES.RX_PRBS_SEL_I[0]")
        self.create_conn(x+25,y+4,"CPE.RAM_O1", x,y,"SERDES.TX_POWER_DOWN_N_I")
        self.create_conn(x+25,y+2,"CPE.RAM_O1", x,y,"SERDES.RX_POWER_DOWN_N_I")
        self.create_conn(x+25,y+0,"CPE.RAM_O1", x,y,"SERDES.TX_ELEC_IDLE_I")

    def create_ram(self, x, y):
        self.create_conn(x-3,y+2,"CPE.RAM_O1", x,y,"RAM.C_ADDRA[0]")
        self.create_conn(x-3,y+2,"CPE.RAM_O2", x,y,"RAM.C_ADDRA[1]")
        self.create_conn(x-3,y+3,"CPE.RAM_O1", x,y,"RAM.C_ADDRA[2]")
        self.create_conn(x-3,y+3,"CPE.RAM_O2", x,y,"RAM.C_ADDRA[3]")
        self.create_conn(x-3,y+4,"CPE.RAM_O1", x,y,"RAM.C_ADDRA[4]")
        self.create_conn(x-3,y+4,"CPE.RAM_O2", x,y,"RAM.C_ADDRA[5]")
        self.create_conn(x-3,y+5,"CPE.RAM_O1", x,y,"RAM.C_ADDRA[6]")
        self.create_conn(x-3,y+5,"CPE.RAM_O2", x,y,"RAM.C_ADDRA[7]")
        self.create_conn(x+2,y+2,"CPE.RAM_O1", x,y,"RAM.C_ADDRB[0]")
        self.create_conn(x+2,y+2,"CPE.RAM_O2", x,y,"RAM.C_ADDRB[1]")
        self.create_conn(x+2,y+3,"CPE.RAM_O1", x,y,"RAM.C_ADDRB[2]")
        self.create_conn(x+2,y+3,"CPE.RAM_O2", x,y,"RAM.C_ADDRB[3]")
        self.create_conn(x+2,y+4,"CPE.RAM_O1", x,y,"RAM.C_ADDRB[4]")
        self.create_conn(x+2,y+4,"CPE.RAM_O2", x,y,"RAM.C_ADDRB[5]")
        self.create_conn(x+2,y+5,"CPE.RAM_O1", x,y,"RAM.C_ADDRB[6]")
        self.create_conn(x+2,y+5,"CPE.RAM_O2", x,y,"RAM.C_ADDRB[7]")
        self.create_conn(x-6,y+0,"CPE.RAM_O1", x,y,"RAM.CLKA[0]")
        self.create_conn(x-3,y+0,"CPE.RAM_O1", x,y,"RAM.CLKA[1]")
        self.create_conn(x-6,y+1,"CPE.RAM_O1", x,y,"RAM.ENA[0]")
        self.create_conn(x-3,y+1,"CPE.RAM_O1", x,y,"RAM.ENA[1]")
        self.create_conn(x-6,y+0,"CPE.RAM_O2", x,y,"RAM.GLWEA[0]")
        self.create_conn(x-3,y+0,"CPE.RAM_O2", x,y,"RAM.GLWEA[1]")
        self.create_conn(x-5,y+0,"CPE.RAM_O1", x,y,"RAM.ADDRA0[0]")
        self.create_conn(x-5,y+0,"CPE.RAM_O2", x,y,"RAM.ADDRA0[1]")
        self.create_conn(x-5,y+1,"CPE.RAM_O1", x,y,"RAM.ADDRA0[2]")
        self.create_conn(x-5,y+1,"CPE.RAM_O2", x,y,"RAM.ADDRA0[3]")
        self.create_conn(x-5,y+2,"CPE.RAM_O1", x,y,"RAM.ADDRA0[4]")
        self.create_conn(x-5,y+2,"CPE.RAM_O2", x,y,"RAM.ADDRA0[5]")
        self.create_conn(x-5,y+3,"CPE.RAM_O1", x,y,"RAM.ADDRA0[6]")
        self.create_conn(x-5,y+3,"CPE.RAM_O2", x,y,"RAM.ADDRA0[7]")
        self.create_conn(x-5,y+4,"CPE.RAM_O1", x,y,"RAM.ADDRA0[8]")
        self.create_conn(x-5,y+4,"CPE.RAM_O2", x,y,"RAM.ADDRA0[9]")
        self.create_conn(x-5,y+5,"CPE.RAM_O1", x,y,"RAM.ADDRA0[10]")
        self.create_conn(x-5,y+5,"CPE.RAM_O2", x,y,"RAM.ADDRA0[11]")
        self.create_conn(x-5,y+6,"CPE.RAM_O1", x,y,"RAM.ADDRA0[12]")
        self.create_conn(x-5,y+6,"CPE.RAM_O2", x,y,"RAM.ADDRA0[13]")
        self.create_conn(x-5,y+7,"CPE.RAM_O1", x,y,"RAM.ADDRA0[14]")
        self.create_conn(x-5,y+7,"CPE.RAM_O2", x,y,"RAM.ADDRA0[15]")
        self.create_conn(x-5,y+0,"CPE.RAM_O1", x,y,"RAM.ADDRA0X[0]")
        self.create_conn(x-4,y+0,"CPE.RAM_O1", x,y,"RAM.ADDRA0X[1]")
        self.create_conn(x-5,y+1,"CPE.RAM_O1", x,y,"RAM.ADDRA0X[2]")
        self.create_conn(x-4,y+1,"CPE.RAM_O1", x,y,"RAM.ADDRA0X[3]")
        self.create_conn(x-5,y+2,"CPE.RAM_O1", x,y,"RAM.ADDRA0X[4]")
        self.create_conn(x-4,y+2,"CPE.RAM_O1", x,y,"RAM.ADDRA0X[5]")
        self.create_conn(x-5,y+3,"CPE.RAM_O1", x,y,"RAM.ADDRA0X[6]")
        self.create_conn(x-4,y+3,"CPE.RAM_O1", x,y,"RAM.ADDRA0X[7]")
        self.create_conn(x-5,y+4,"CPE.RAM_O1", x,y,"RAM.ADDRA0X[8]")
        self.create_conn(x-4,y+4,"CPE.RAM_O1", x,y,"RAM.ADDRA0X[9]")
        self.create_conn(x-5,y+5,"CPE.RAM_O1", x,y,"RAM.ADDRA0X[10]")
        self.create_conn(x-4,y+5,"CPE.RAM_O1", x,y,"RAM.ADDRA0X[11]")
        self.create_conn(x-6,y+6,"CPE.RAM_O1", x,y,"RAM.ADDRA0X[12]")
        self.create_conn(x-5,y+6,"CPE.RAM_O1", x,y,"RAM.ADDRA0X[13]")
        self.create_conn(x-6,y+7,"CPE.RAM_O1", x,y,"RAM.ADDRA0X[14]")
        self.create_conn(x-5,y+7,"CPE.RAM_O1", x,y,"RAM.ADDRA0X[15]")
        self.create_conn(x-1,y+0,"CPE.RAM_O1", x,y,"RAM.DIA[0]")
        self.create_conn(x-1,y+0,"CPE.RAM_O2", x,y,"RAM.DIA[1]")
        self.create_conn(x-1,y+1,"CPE.RAM_O1", x,y,"RAM.DIA[2]")
        self.create_conn(x-1,y+1,"CPE.RAM_O2", x,y,"RAM.DIA[3]")
        self.create_conn(x-1,y+2,"CPE.RAM_O1", x,y,"RAM.DIA[4]")
        self.create_conn(x-1,y+2,"CPE.RAM_O2", x,y,"RAM.DIA[5]")
        self.create_conn(x-1,y+3,"CPE.RAM_O1", x,y,"RAM.DIA[6]")
        self.create_conn(x-1,y+3,"CPE.RAM_O2", x,y,"RAM.DIA[7]")
        self.create_conn(x-1,y+4,"CPE.RAM_O1", x,y,"RAM.DIA[8]")
        self.create_conn(x-1,y+4,"CPE.RAM_O2", x,y,"RAM.DIA[9]")
        self.create_conn(x-1,y+5,"CPE.RAM_O1", x,y,"RAM.DIA[10]")
        self.create_conn(x-1,y+5,"CPE.RAM_O2", x,y,"RAM.DIA[11]")
        self.create_conn(x-1,y+6,"CPE.RAM_O1", x,y,"RAM.DIA[12]")
        self.create_conn(x-1,y+6,"CPE.RAM_O2", x,y,"RAM.DIA[13]")
        self.create_conn(x-1,y+7,"CPE.RAM_O1", x,y,"RAM.DIA[14]")
        self.create_conn(x-1,y+7,"CPE.RAM_O2", x,y,"RAM.DIA[15]")
        self.create_conn(x-3,y+6,"CPE.RAM_O1", x,y,"RAM.DIA[16]")
        self.create_conn(x-3,y+6,"CPE.RAM_O2", x,y,"RAM.DIA[17]")
        self.create_conn(x-3,y+7,"CPE.RAM_O1", x,y,"RAM.DIA[18]")
        self.create_conn(x-3,y+7,"CPE.RAM_O2", x,y,"RAM.DIA[19]")
        self.create_conn(x-2,y+0,"CPE.RAM_O1", x,y,"RAM.WEA[0]")
        self.create_conn(x-2,y+0,"CPE.RAM_O2", x,y,"RAM.WEA[1]")
        self.create_conn(x-2,y+1,"CPE.RAM_O1", x,y,"RAM.WEA[2]")
        self.create_conn(x-2,y+1,"CPE.RAM_O2", x,y,"RAM.WEA[3]")
        self.create_conn(x-2,y+2,"CPE.RAM_O1", x,y,"RAM.WEA[4]")
        self.create_conn(x-2,y+2,"CPE.RAM_O2", x,y,"RAM.WEA[5]")
        self.create_conn(x-2,y+3,"CPE.RAM_O1", x,y,"RAM.WEA[6]")
        self.create_conn(x-2,y+3,"CPE.RAM_O2", x,y,"RAM.WEA[7]")
        self.create_conn(x-2,y+4,"CPE.RAM_O1", x,y,"RAM.WEA[8]")
        self.create_conn(x-2,y+4,"CPE.RAM_O2", x,y,"RAM.WEA[9]")
        self.create_conn(x-2,y+5,"CPE.RAM_O1", x,y,"RAM.WEA[10]")
        self.create_conn(x-2,y+5,"CPE.RAM_O2", x,y,"RAM.WEA[11]")
        self.create_conn(x-2,y+6,"CPE.RAM_O1", x,y,"RAM.WEA[12]")
        self.create_conn(x-2,y+6,"CPE.RAM_O2", x,y,"RAM.WEA[13]")
        self.create_conn(x-2,y+7,"CPE.RAM_O1", x,y,"RAM.WEA[14]")
        self.create_conn(x-2,y+7,"CPE.RAM_O2", x,y,"RAM.WEA[15]")
        self.create_conn(x-4,y+6,"CPE.RAM_O1", x,y,"RAM.WEA[16]")
        self.create_conn(x-4,y+6,"CPE.RAM_O2", x,y,"RAM.WEA[17]")
        self.create_conn(x-4,y+7,"CPE.RAM_O1", x,y,"RAM.WEA[18]")
        self.create_conn(x-4,y+7,"CPE.RAM_O2", x,y,"RAM.WEA[19]")
        self.create_conn(x-6,y+8,"CPE.RAM_O1", x,y,"RAM.CLKA[2]")
        self.create_conn(x-3,y+8,"CPE.RAM_O1", x,y,"RAM.CLKA[3]")
        self.create_conn(x-6,y+9,"CPE.RAM_O1", x,y,"RAM.ENA[2]")
        self.create_conn(x-3,y+9,"CPE.RAM_O1", x,y,"RAM.ENA[3]")
        self.create_conn(x-6,y+8,"CPE.RAM_O2", x,y,"RAM.GLWEA[2]")
        self.create_conn(x-3,y+8,"CPE.RAM_O2", x,y,"RAM.GLWEA[3]")
        self.create_conn(x-5,y+8,"CPE.RAM_O1", x,y,"RAM.ADDRA1[0]")
        self.create_conn(x-5,y+8,"CPE.RAM_O2", x,y,"RAM.ADDRA1[1]")
        self.create_conn(x-5,y+9,"CPE.RAM_O1", x,y,"RAM.ADDRA1[2]")
        self.create_conn(x-5,y+9,"CPE.RAM_O2", x,y,"RAM.ADDRA1[3]")
        self.create_conn(x-5,y+10,"CPE.RAM_O1", x,y,"RAM.ADDRA1[4]")
        self.create_conn(x-5,y+10,"CPE.RAM_O2", x,y,"RAM.ADDRA1[5]")
        self.create_conn(x-5,y+11,"CPE.RAM_O1", x,y,"RAM.ADDRA1[6]")
        self.create_conn(x-5,y+11,"CPE.RAM_O2", x,y,"RAM.ADDRA1[7]")
        self.create_conn(x-5,y+12,"CPE.RAM_O1", x,y,"RAM.ADDRA1[8]")
        self.create_conn(x-5,y+12,"CPE.RAM_O2", x,y,"RAM.ADDRA1[9]")
        self.create_conn(x-5,y+13,"CPE.RAM_O1", x,y,"RAM.ADDRA1[10]")
        self.create_conn(x-5,y+13,"CPE.RAM_O2", x,y,"RAM.ADDRA1[11]")
        self.create_conn(x-5,y+14,"CPE.RAM_O1", x,y,"RAM.ADDRA1[12]")
        self.create_conn(x-5,y+14,"CPE.RAM_O2", x,y,"RAM.ADDRA1[13]")
        self.create_conn(x-5,y+15,"CPE.RAM_O1", x,y,"RAM.ADDRA1[14]")
        self.create_conn(x-5,y+15,"CPE.RAM_O2", x,y,"RAM.ADDRA1[15]")
        self.create_conn(x-5,y+8,"CPE.RAM_O1", x,y,"RAM.ADDRA1X[0]")
        self.create_conn(x-4,y+8,"CPE.RAM_O1", x,y,"RAM.ADDRA1X[1]")
        self.create_conn(x-5,y+9,"CPE.RAM_O1", x,y,"RAM.ADDRA1X[2]")
        self.create_conn(x-4,y+9,"CPE.RAM_O1", x,y,"RAM.ADDRA1X[3]")
        self.create_conn(x-5,y+10,"CPE.RAM_O1", x,y,"RAM.ADDRA1X[4]")
        self.create_conn(x-4,y+10,"CPE.RAM_O1", x,y,"RAM.ADDRA1X[5]")
        self.create_conn(x-5,y+11,"CPE.RAM_O1", x,y,"RAM.ADDRA1X[6]")
        self.create_conn(x-4,y+11,"CPE.RAM_O1", x,y,"RAM.ADDRA1X[7]")
        self.create_conn(x-5,y+12,"CPE.RAM_O1", x,y,"RAM.ADDRA1X[8]")
        self.create_conn(x-4,y+12,"CPE.RAM_O1", x,y,"RAM.ADDRA1X[9]")
        self.create_conn(x-5,y+13,"CPE.RAM_O1", x,y,"RAM.ADDRA1X[10]")
        self.create_conn(x-4,y+13,"CPE.RAM_O1", x,y,"RAM.ADDRA1X[11]")
        self.create_conn(x-6,y+14,"CPE.RAM_O1", x,y,"RAM.ADDRA1X[12]")
        self.create_conn(x-5,y+14,"CPE.RAM_O1", x,y,"RAM.ADDRA1X[13]")
        self.create_conn(x-6,y+15,"CPE.RAM_O1", x,y,"RAM.ADDRA1X[14]")
        self.create_conn(x-5,y+15,"CPE.RAM_O1", x,y,"RAM.ADDRA1X[15]")
        self.create_conn(x-1,y+8,"CPE.RAM_O1", x,y,"RAM.DIA[20]")
        self.create_conn(x-1,y+8,"CPE.RAM_O2", x,y,"RAM.DIA[21]")
        self.create_conn(x-1,y+9,"CPE.RAM_O1", x,y,"RAM.DIA[22]")
        self.create_conn(x-1,y+9,"CPE.RAM_O2", x,y,"RAM.DIA[23]")
        self.create_conn(x-1,y+10,"CPE.RAM_O1", x,y,"RAM.DIA[24]")
        self.create_conn(x-1,y+10,"CPE.RAM_O2", x,y,"RAM.DIA[25]")
        self.create_conn(x-1,y+11,"CPE.RAM_O1", x,y,"RAM.DIA[26]")
        self.create_conn(x-1,y+11,"CPE.RAM_O2", x,y,"RAM.DIA[27]")
        self.create_conn(x-1,y+12,"CPE.RAM_O1", x,y,"RAM.DIA[28]")
        self.create_conn(x-1,y+12,"CPE.RAM_O2", x,y,"RAM.DIA[29]")
        self.create_conn(x-1,y+13,"CPE.RAM_O1", x,y,"RAM.DIA[30]")
        self.create_conn(x-1,y+13,"CPE.RAM_O2", x,y,"RAM.DIA[31]")
        self.create_conn(x-1,y+14,"CPE.RAM_O1", x,y,"RAM.DIA[32]")
        self.create_conn(x-1,y+14,"CPE.RAM_O2", x,y,"RAM.DIA[33]")
        self.create_conn(x-1,y+15,"CPE.RAM_O1", x,y,"RAM.DIA[34]")
        self.create_conn(x-1,y+15,"CPE.RAM_O2", x,y,"RAM.DIA[35]")
        self.create_conn(x-3,y+14,"CPE.RAM_O1", x,y,"RAM.DIA[36]")
        self.create_conn(x-3,y+14,"CPE.RAM_O2", x,y,"RAM.DIA[37]")
        self.create_conn(x-3,y+15,"CPE.RAM_O1", x,y,"RAM.DIA[38]")
        self.create_conn(x-3,y+15,"CPE.RAM_O2", x,y,"RAM.DIA[39]")
        self.create_conn(x-2,y+8,"CPE.RAM_O1", x,y,"RAM.WEA[20]")
        self.create_conn(x-2,y+8,"CPE.RAM_O2", x,y,"RAM.WEA[21]")
        self.create_conn(x-2,y+9,"CPE.RAM_O1", x,y,"RAM.WEA[22]")
        self.create_conn(x-2,y+9,"CPE.RAM_O2", x,y,"RAM.WEA[23]")
        self.create_conn(x-2,y+10,"CPE.RAM_O1", x,y,"RAM.WEA[24]")
        self.create_conn(x-2,y+10,"CPE.RAM_O2", x,y,"RAM.WEA[25]")
        self.create_conn(x-2,y+11,"CPE.RAM_O1", x,y,"RAM.WEA[26]")
        self.create_conn(x-2,y+11,"CPE.RAM_O2", x,y,"RAM.WEA[27]")
        self.create_conn(x-2,y+12,"CPE.RAM_O1", x,y,"RAM.WEA[28]")
        self.create_conn(x-2,y+12,"CPE.RAM_O2", x,y,"RAM.WEA[29]")
        self.create_conn(x-2,y+13,"CPE.RAM_O1", x,y,"RAM.WEA[30]")
        self.create_conn(x-2,y+13,"CPE.RAM_O2", x,y,"RAM.WEA[31]")
        self.create_conn(x-2,y+14,"CPE.RAM_O1", x,y,"RAM.WEA[32]")
        self.create_conn(x-2,y+14,"CPE.RAM_O2", x,y,"RAM.WEA[33]")
        self.create_conn(x-2,y+15,"CPE.RAM_O1", x,y,"RAM.WEA[34]")
        self.create_conn(x-2,y+15,"CPE.RAM_O2", x,y,"RAM.WEA[35]")
        self.create_conn(x-4,y+14,"CPE.RAM_O1", x,y,"RAM.WEA[36]")
        self.create_conn(x-4,y+14,"CPE.RAM_O2", x,y,"RAM.WEA[37]")
        self.create_conn(x-4,y+15,"CPE.RAM_O1", x,y,"RAM.WEA[38]")
        self.create_conn(x-4,y+15,"CPE.RAM_O2", x,y,"RAM.WEA[39]")
        self.create_conn(x+2,y+0,"CPE.RAM_O1", x,y,"RAM.CLKB[0]")
        self.create_conn(x+5,y+0,"CPE.RAM_O1", x,y,"RAM.CLKB[1]")
        self.create_conn(x+2,y+1,"CPE.RAM_O1", x,y,"RAM.ENB[0]")
        self.create_conn(x+5,y+1,"CPE.RAM_O1", x,y,"RAM.ENB[1]")
        self.create_conn(x+2,y+0,"CPE.RAM_O2", x,y,"RAM.GLWEB[0]")
        self.create_conn(x+5,y+0,"CPE.RAM_O2", x,y,"RAM.GLWEB[1]")
        self.create_conn(x+4,y+0,"CPE.RAM_O1", x,y,"RAM.ADDRB0[0]")
        self.create_conn(x+4,y+0,"CPE.RAM_O2", x,y,"RAM.ADDRB0[1]")
        self.create_conn(x+4,y+1,"CPE.RAM_O1", x,y,"RAM.ADDRB0[2]")
        self.create_conn(x+4,y+1,"CPE.RAM_O2", x,y,"RAM.ADDRB0[3]")
        self.create_conn(x+4,y+2,"CPE.RAM_O1", x,y,"RAM.ADDRB0[4]")
        self.create_conn(x+4,y+2,"CPE.RAM_O2", x,y,"RAM.ADDRB0[5]")
        self.create_conn(x+4,y+3,"CPE.RAM_O1", x,y,"RAM.ADDRB0[6]")
        self.create_conn(x+4,y+3,"CPE.RAM_O2", x,y,"RAM.ADDRB0[7]")
        self.create_conn(x+4,y+4,"CPE.RAM_O1", x,y,"RAM.ADDRB0[8]")
        self.create_conn(x+4,y+4,"CPE.RAM_O2", x,y,"RAM.ADDRB0[9]")
        self.create_conn(x+4,y+5,"CPE.RAM_O1", x,y,"RAM.ADDRB0[10]")
        self.create_conn(x+4,y+5,"CPE.RAM_O2", x,y,"RAM.ADDRB0[11]")
        self.create_conn(x+4,y+6,"CPE.RAM_O1", x,y,"RAM.ADDRB0[12]")
        self.create_conn(x+4,y+6,"CPE.RAM_O2", x,y,"RAM.ADDRB0[13]")
        self.create_conn(x+4,y+7,"CPE.RAM_O1", x,y,"RAM.ADDRB0[14]")
        self.create_conn(x+4,y+7,"CPE.RAM_O2", x,y,"RAM.ADDRB0[15]")
        self.create_conn(x+3,y+0,"CPE.RAM_O1", x,y,"RAM.ADDRB0X[0]")
        self.create_conn(x+4,y+0,"CPE.RAM_O1", x,y,"RAM.ADDRB0X[1]")
        self.create_conn(x+3,y+1,"CPE.RAM_O1", x,y,"RAM.ADDRB0X[2]")
        self.create_conn(x+4,y+1,"CPE.RAM_O1", x,y,"RAM.ADDRB0X[3]")
        self.create_conn(x+3,y+2,"CPE.RAM_O1", x,y,"RAM.ADDRB0X[4]")
        self.create_conn(x+4,y+2,"CPE.RAM_O1", x,y,"RAM.ADDRB0X[5]")
        self.create_conn(x+3,y+3,"CPE.RAM_O1", x,y,"RAM.ADDRB0X[6]")
        self.create_conn(x+4,y+3,"CPE.RAM_O1", x,y,"RAM.ADDRB0X[7]")
        self.create_conn(x+3,y+4,"CPE.RAM_O1", x,y,"RAM.ADDRB0X[8]")
        self.create_conn(x+4,y+4,"CPE.RAM_O1", x,y,"RAM.ADDRB0X[9]")
        self.create_conn(x+3,y+5,"CPE.RAM_O1", x,y,"RAM.ADDRB0X[10]")
        self.create_conn(x+4,y+5,"CPE.RAM_O1", x,y,"RAM.ADDRB0X[11]")
        self.create_conn(x+4,y+6,"CPE.RAM_O1", x,y,"RAM.ADDRB0X[12]")
        self.create_conn(x+5,y+6,"CPE.RAM_O1", x,y,"RAM.ADDRB0X[13]")
        self.create_conn(x+4,y+7,"CPE.RAM_O1", x,y,"RAM.ADDRB0X[14]")
        self.create_conn(x+5,y+7,"CPE.RAM_O1", x,y,"RAM.ADDRB0X[15]")
        self.create_conn(x+1,y+0,"CPE.RAM_O1", x,y,"RAM.DIB[0]")
        self.create_conn(x+1,y+0,"CPE.RAM_O2", x,y,"RAM.DIB[1]")
        self.create_conn(x+1,y+1,"CPE.RAM_O1", x,y,"RAM.DIB[2]")
        self.create_conn(x+1,y+1,"CPE.RAM_O2", x,y,"RAM.DIB[3]")
        self.create_conn(x+1,y+2,"CPE.RAM_O1", x,y,"RAM.DIB[4]")
        self.create_conn(x+1,y+2,"CPE.RAM_O2", x,y,"RAM.DIB[5]")
        self.create_conn(x+1,y+3,"CPE.RAM_O1", x,y,"RAM.DIB[6]")
        self.create_conn(x+1,y+3,"CPE.RAM_O2", x,y,"RAM.DIB[7]")
        self.create_conn(x+1,y+4,"CPE.RAM_O1", x,y,"RAM.DIB[8]")
        self.create_conn(x+1,y+4,"CPE.RAM_O2", x,y,"RAM.DIB[9]")
        self.create_conn(x+1,y+5,"CPE.RAM_O1", x,y,"RAM.DIB[10]")
        self.create_conn(x+1,y+5,"CPE.RAM_O2", x,y,"RAM.DIB[11]")
        self.create_conn(x+1,y+6,"CPE.RAM_O1", x,y,"RAM.DIB[12]")
        self.create_conn(x+1,y+6,"CPE.RAM_O2", x,y,"RAM.DIB[13]")
        self.create_conn(x+1,y+7,"CPE.RAM_O1", x,y,"RAM.DIB[14]")
        self.create_conn(x+1,y+7,"CPE.RAM_O2", x,y,"RAM.DIB[15]")
        self.create_conn(x+3,y+6,"CPE.RAM_O1", x,y,"RAM.DIB[16]")
        self.create_conn(x+3,y+6,"CPE.RAM_O2", x,y,"RAM.DIB[17]")
        self.create_conn(x+3,y+7,"CPE.RAM_O1", x,y,"RAM.DIB[18]")
        self.create_conn(x+3,y+7,"CPE.RAM_O2", x,y,"RAM.DIB[19]")
        self.create_conn(x+0,y+0,"CPE.RAM_O1", x,y,"RAM.WEB[0]")
        self.create_conn(x+0,y+0,"CPE.RAM_O2", x,y,"RAM.WEB[1]")
        self.create_conn(x+0,y+1,"CPE.RAM_O1", x,y,"RAM.WEB[2]")
        self.create_conn(x+0,y+1,"CPE.RAM_O2", x,y,"RAM.WEB[3]")
        self.create_conn(x+0,y+2,"CPE.RAM_O1", x,y,"RAM.WEB[4]")
        self.create_conn(x+0,y+2,"CPE.RAM_O2", x,y,"RAM.WEB[5]")
        self.create_conn(x+0,y+3,"CPE.RAM_O1", x,y,"RAM.WEB[6]")
        self.create_conn(x+0,y+3,"CPE.RAM_O2", x,y,"RAM.WEB[7]")
        self.create_conn(x+0,y+4,"CPE.RAM_O1", x,y,"RAM.WEB[8]")
        self.create_conn(x+0,y+4,"CPE.RAM_O2", x,y,"RAM.WEB[9]")
        self.create_conn(x+0,y+5,"CPE.RAM_O1", x,y,"RAM.WEB[10]")
        self.create_conn(x+0,y+5,"CPE.RAM_O2", x,y,"RAM.WEB[11]")
        self.create_conn(x+0,y+6,"CPE.RAM_O1", x,y,"RAM.WEB[12]")
        self.create_conn(x+0,y+6,"CPE.RAM_O2", x,y,"RAM.WEB[13]")
        self.create_conn(x+0,y+7,"CPE.RAM_O1", x,y,"RAM.WEB[14]")
        self.create_conn(x+0,y+7,"CPE.RAM_O2", x,y,"RAM.WEB[15]")
        self.create_conn(x+2,y+6,"CPE.RAM_O1", x,y,"RAM.WEB[16]")
        self.create_conn(x+2,y+6,"CPE.RAM_O2", x,y,"RAM.WEB[17]")
        self.create_conn(x+2,y+7,"CPE.RAM_O1", x,y,"RAM.WEB[18]")
        self.create_conn(x+2,y+7,"CPE.RAM_O2", x,y,"RAM.WEB[19]")
        self.create_conn(x+2,y+8,"CPE.RAM_O1", x,y,"RAM.CLKB[2]")
        self.create_conn(x+5,y+8,"CPE.RAM_O1", x,y,"RAM.CLKB[3]")
        self.create_conn(x+2,y+9,"CPE.RAM_O1", x,y,"RAM.ENB[2]")
        self.create_conn(x+5,y+9,"CPE.RAM_O1", x,y,"RAM.ENB[3]")
        self.create_conn(x+2,y+8,"CPE.RAM_O2", x,y,"RAM.GLWEB[2]")
        self.create_conn(x+5,y+8,"CPE.RAM_O2", x,y,"RAM.GLWEB[3]")
        self.create_conn(x+4,y+8,"CPE.RAM_O1", x,y,"RAM.ADDRB1[0]")
        self.create_conn(x+4,y+8,"CPE.RAM_O2", x,y,"RAM.ADDRB1[1]")
        self.create_conn(x+4,y+9,"CPE.RAM_O1", x,y,"RAM.ADDRB1[2]")
        self.create_conn(x+4,y+9,"CPE.RAM_O2", x,y,"RAM.ADDRB1[3]")
        self.create_conn(x+4,y+10,"CPE.RAM_O1", x,y,"RAM.ADDRB1[4]")
        self.create_conn(x+4,y+10,"CPE.RAM_O2", x,y,"RAM.ADDRB1[5]")
        self.create_conn(x+4,y+11,"CPE.RAM_O1", x,y,"RAM.ADDRB1[6]")
        self.create_conn(x+4,y+11,"CPE.RAM_O2", x,y,"RAM.ADDRB1[7]")
        self.create_conn(x+4,y+12,"CPE.RAM_O1", x,y,"RAM.ADDRB1[8]")
        self.create_conn(x+4,y+12,"CPE.RAM_O2", x,y,"RAM.ADDRB1[9]")
        self.create_conn(x+4,y+13,"CPE.RAM_O1", x,y,"RAM.ADDRB1[10]")
        self.create_conn(x+4,y+13,"CPE.RAM_O2", x,y,"RAM.ADDRB1[11]")
        self.create_conn(x+4,y+14,"CPE.RAM_O1", x,y,"RAM.ADDRB1[12]")
        self.create_conn(x+4,y+14,"CPE.RAM_O2", x,y,"RAM.ADDRB1[13]")
        self.create_conn(x+4,y+15,"CPE.RAM_O1", x,y,"RAM.ADDRB1[14]")
        self.create_conn(x+4,y+15,"CPE.RAM_O2", x,y,"RAM.ADDRB1[15]")
        self.create_conn(x+3,y+8,"CPE.RAM_O1", x,y,"RAM.ADDRB1X[0]")
        self.create_conn(x+4,y+8,"CPE.RAM_O1", x,y,"RAM.ADDRB1X[1]")
        self.create_conn(x+3,y+9,"CPE.RAM_O1", x,y,"RAM.ADDRB1X[2]")
        self.create_conn(x+4,y+9,"CPE.RAM_O1", x,y,"RAM.ADDRB1X[3]")
        self.create_conn(x+3,y+10,"CPE.RAM_O1", x,y,"RAM.ADDRB1X[4]")
        self.create_conn(x+4,y+10,"CPE.RAM_O1", x,y,"RAM.ADDRB1X[5]")
        self.create_conn(x+3,y+11,"CPE.RAM_O1", x,y,"RAM.ADDRB1X[6]")
        self.create_conn(x+4,y+11,"CPE.RAM_O1", x,y,"RAM.ADDRB1X[7]")
        self.create_conn(x+3,y+12,"CPE.RAM_O1", x,y,"RAM.ADDRB1X[8]")
        self.create_conn(x+4,y+12,"CPE.RAM_O1", x,y,"RAM.ADDRB1X[9]")
        self.create_conn(x+3,y+13,"CPE.RAM_O1", x,y,"RAM.ADDRB1X[10]")
        self.create_conn(x+4,y+13,"CPE.RAM_O1", x,y,"RAM.ADDRB1X[11]")
        self.create_conn(x+4,y+14,"CPE.RAM_O1", x,y,"RAM.ADDRB1X[12]")
        self.create_conn(x+5,y+14,"CPE.RAM_O1", x,y,"RAM.ADDRB1X[13]")
        self.create_conn(x+4,y+15,"CPE.RAM_O1", x,y,"RAM.ADDRB1X[14]")
        self.create_conn(x+5,y+15,"CPE.RAM_O1", x,y,"RAM.ADDRB1X[15]")
        self.create_conn(x+1,y+8,"CPE.RAM_O1", x,y,"RAM.DIB[20]")
        self.create_conn(x+1,y+8,"CPE.RAM_O2", x,y,"RAM.DIB[21]")
        self.create_conn(x+1,y+9,"CPE.RAM_O1", x,y,"RAM.DIB[22]")
        self.create_conn(x+1,y+9,"CPE.RAM_O2", x,y,"RAM.DIB[23]")
        self.create_conn(x+1,y+10,"CPE.RAM_O1", x,y,"RAM.DIB[24]")
        self.create_conn(x+1,y+10,"CPE.RAM_O2", x,y,"RAM.DIB[25]")
        self.create_conn(x+1,y+11,"CPE.RAM_O1", x,y,"RAM.DIB[26]")
        self.create_conn(x+1,y+11,"CPE.RAM_O2", x,y,"RAM.DIB[27]")
        self.create_conn(x+1,y+12,"CPE.RAM_O1", x,y,"RAM.DIB[28]")
        self.create_conn(x+1,y+12,"CPE.RAM_O2", x,y,"RAM.DIB[29]")
        self.create_conn(x+1,y+13,"CPE.RAM_O1", x,y,"RAM.DIB[30]")
        self.create_conn(x+1,y+13,"CPE.RAM_O2", x,y,"RAM.DIB[31]")
        self.create_conn(x+1,y+14,"CPE.RAM_O1", x,y,"RAM.DIB[32]")
        self.create_conn(x+1,y+14,"CPE.RAM_O2", x,y,"RAM.DIB[33]")
        self.create_conn(x+1,y+15,"CPE.RAM_O1", x,y,"RAM.DIB[34]")
        self.create_conn(x+1,y+15,"CPE.RAM_O2", x,y,"RAM.DIB[35]")
        self.create_conn(x+3,y+14,"CPE.RAM_O1", x,y,"RAM.DIB[36]")
        self.create_conn(x+3,y+14,"CPE.RAM_O2", x,y,"RAM.DIB[37]")
        self.create_conn(x+3,y+15,"CPE.RAM_O1", x,y,"RAM.DIB[38]")
        self.create_conn(x+3,y+15,"CPE.RAM_O2", x,y,"RAM.DIB[39]")
        self.create_conn(x+0,y+8,"CPE.RAM_O1", x,y,"RAM.WEB[20]")
        self.create_conn(x+0,y+8,"CPE.RAM_O2", x,y,"RAM.WEB[21]")
        self.create_conn(x+0,y+9,"CPE.RAM_O1", x,y,"RAM.WEB[22]")
        self.create_conn(x+0,y+9,"CPE.RAM_O2", x,y,"RAM.WEB[23]")
        self.create_conn(x+0,y+10,"CPE.RAM_O1", x,y,"RAM.WEB[24]")
        self.create_conn(x+0,y+10,"CPE.RAM_O2", x,y,"RAM.WEB[25]")
        self.create_conn(x+0,y+11,"CPE.RAM_O1", x,y,"RAM.WEB[26]")
        self.create_conn(x+0,y+11,"CPE.RAM_O2", x,y,"RAM.WEB[27]")
        self.create_conn(x+0,y+12,"CPE.RAM_O1", x,y,"RAM.WEB[28]")
        self.create_conn(x+0,y+12,"CPE.RAM_O2", x,y,"RAM.WEB[29]")
        self.create_conn(x+0,y+13,"CPE.RAM_O1", x,y,"RAM.WEB[30]")
        self.create_conn(x+0,y+13,"CPE.RAM_O2", x,y,"RAM.WEB[31]")
        self.create_conn(x+0,y+14,"CPE.RAM_O1", x,y,"RAM.WEB[32]")
        self.create_conn(x+0,y+14,"CPE.RAM_O2", x,y,"RAM.WEB[33]")
        self.create_conn(x+0,y+15,"CPE.RAM_O1", x,y,"RAM.WEB[34]")
        self.create_conn(x+0,y+15,"CPE.RAM_O2", x,y,"RAM.WEB[35]")
        self.create_conn(x+2,y+14,"CPE.RAM_O1", x,y,"RAM.WEB[36]")
        self.create_conn(x+2,y+14,"CPE.RAM_O2", x,y,"RAM.WEB[37]")
        self.create_conn(x+2,y+15,"CPE.RAM_O1", x,y,"RAM.WEB[38]")
        self.create_conn(x+2,y+15,"CPE.RAM_O2", x,y,"RAM.WEB[39]")
        self.create_conn(x-6,y+2,"CPE.RAM_O2", x,y,"RAM.F_RSTN")
        self.create_conn(x,y,"RAM.DOA[0]", x-1,y+0,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOAX[0]", x-2,y+0,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[1]", x-1,y+0,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOAX[1]", x-1,y+0,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[2]", x-1,y+1,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOAX[2]", x-2,y+1,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[3]", x-1,y+1,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOAX[3]", x-1,y+1,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[4]", x-1,y+2,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOAX[4]", x-2,y+2,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[5]", x-1,y+2,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOAX[5]", x-1,y+2,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[6]", x-1,y+3,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOAX[6]", x-2,y+3,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[7]", x-1,y+3,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOAX[7]", x-1,y+3,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[8]", x-1,y+4,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOAX[8]", x-2,y+4,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[9]", x-1,y+4,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOAX[9]", x-1,y+4,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[10]", x-1,y+5,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOAX[10]", x-2,y+5,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[11]", x-1,y+5,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOAX[11]", x-1,y+5,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[12]", x-1,y+6,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOAX[12]", x-2,y+6,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[13]", x-1,y+6,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOAX[13]", x-1,y+6,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[14]", x-1,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOAX[14]", x-2,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[15]", x-1,y+7,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOAX[15]", x-1,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[16]", x-3,y+6,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOAX[16]", x-4,y+6,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[17]", x-3,y+6,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOAX[17]", x-3,y+6,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[18]", x-3,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOAX[18]", x-4,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[19]", x-3,y+7,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOAX[19]", x-3,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[20]", x-1,y+8,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOAX[20]", x-2,y+8,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[21]", x-1,y+8,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOAX[21]", x-1,y+8,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[22]", x-1,y+9,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOAX[22]", x-2,y+9,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[23]", x-1,y+9,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOAX[23]", x-1,y+9,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[24]", x-1,y+10,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOAX[24]", x-2,y+10,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[25]", x-1,y+10,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOAX[25]", x-1,y+10,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[26]", x-1,y+11,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOAX[26]", x-2,y+11,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[27]", x-1,y+11,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOAX[27]", x-1,y+11,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[28]", x-1,y+12,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOAX[28]", x-2,y+12,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[29]", x-1,y+12,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOAX[29]", x-1,y+12,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[30]", x-1,y+13,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOAX[30]", x-2,y+13,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[31]", x-1,y+13,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOAX[31]", x-1,y+13,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[32]", x-1,y+14,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOAX[32]", x-2,y+14,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[33]", x-1,y+14,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOAX[33]", x-1,y+14,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[34]", x-1,y+15,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOAX[34]", x-2,y+15,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[35]", x-1,y+15,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOAX[35]", x-1,y+15,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[36]", x-3,y+14,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOAX[36]", x-4,y+14,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[37]", x-3,y+14,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOAX[37]", x-3,y+14,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[38]", x-3,y+15,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOAX[38]", x-4,y+15,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOA[39]", x-3,y+15,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOAX[39]", x-3,y+15,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.CLOCKA[1]", x-3,y+10,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.CLOCKA[2]", x-3,y+11,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.CLOCKA[3]", x-3,y+12,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.CLOCKA[4]", x-3,y+13,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOB[0]", x+1,y+0,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOBX[0]", x+0,y+0,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[1]", x+1,y+0,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOBX[1]", x+1,y+0,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[2]", x+1,y+1,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOBX[2]", x+0,y+1,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[3]", x+1,y+1,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOBX[3]", x+1,y+1,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[4]", x+1,y+2,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOBX[4]", x+0,y+2,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[5]", x+1,y+2,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOBX[5]", x+1,y+2,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[6]", x+1,y+3,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOBX[6]", x+0,y+3,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[7]", x+1,y+3,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOBX[7]", x+1,y+3,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[8]", x+1,y+4,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOBX[8]", x+0,y+4,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[9]", x+1,y+4,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOBX[9]", x+1,y+4,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[10]", x+1,y+5,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOBX[10]", x+0,y+5,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[11]", x+1,y+5,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOBX[11]", x+1,y+5,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[12]", x+1,y+6,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOBX[12]", x+0,y+6,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[13]", x+1,y+6,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOBX[13]", x+1,y+6,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[14]", x+1,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOBX[14]", x+0,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[15]", x+1,y+7,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOBX[15]", x+1,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[16]", x+3,y+6,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOBX[16]", x+2,y+6,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[17]", x+3,y+6,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOBX[17]", x+3,y+6,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[18]", x+3,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOBX[18]", x+2,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[19]", x+3,y+7,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOBX[19]", x+3,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[20]", x+1,y+8,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOBX[20]", x+0,y+8,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[21]", x+1,y+8,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOBX[21]", x+1,y+8,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[22]", x+1,y+9,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOBX[22]", x+0,y+9,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[23]", x+1,y+9,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOBX[23]", x+1,y+9,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[24]", x+1,y+10,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOBX[24]", x+0,y+10,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[25]", x+1,y+10,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOBX[25]", x+1,y+10,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[26]", x+1,y+11,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOBX[26]", x+0,y+11,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[27]", x+1,y+11,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOBX[27]", x+1,y+11,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[28]", x+1,y+12,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOBX[28]", x+0,y+12,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[29]", x+1,y+12,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOBX[29]", x+1,y+12,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[30]", x+1,y+13,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOBX[30]", x+0,y+13,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[31]", x+1,y+13,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOBX[31]", x+1,y+13,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[32]", x+1,y+14,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOBX[32]", x+0,y+14,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[33]", x+1,y+14,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOBX[33]", x+1,y+14,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[34]", x+1,y+15,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOBX[34]", x+0,y+15,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[35]", x+1,y+15,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOBX[35]", x+1,y+15,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[36]", x+3,y+14,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOBX[36]", x+2,y+14,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[37]", x+3,y+14,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOBX[37]", x+3,y+14,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[38]", x+3,y+15,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.DOBX[38]", x+2,y+15,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.DOB[39]", x+3,y+15,"CPE.RAM_I2")
#       self.create_conn(x,y,"RAM.DOBX[39]", x+3,y+15,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.CLOCKB[1]", x+2,y+10,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.CLOCKB[2]", x+2,y+11,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.CLOCKB[3]", x+2,y+12,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.CLOCKB[4]", x+2,y+13,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.ECC1B_ERRA[0]", x-4,y+0,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.ECC1B_ERRA[1]", x-4,y+8,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.ECC1B_ERRA[2]", x+5,y+0,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.ECC1B_ERRA[3]", x+5,y+8,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.ECC1B_ERRB[0]", x-4,y+1,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.ECC1B_ERRB[1]", x-4,y+9,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.ECC1B_ERRB[2]", x+5,y+1,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.ECC1B_ERRB[3]", x+5,y+9,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.ECC2B_ERRA[0]", x-4,y+0,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.ECC2B_ERRA[1]", x-4,y+8,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.ECC2B_ERRA[2]", x+5,y+0,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.ECC2B_ERRA[3]", x+5,y+8,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.ECC2B_ERRB[0]", x-4,y+1,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.ECC2B_ERRB[1]", x-4,y+9,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.ECC2B_ERRB[2]", x+5,y+1,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.ECC2B_ERRB[3]", x+5,y+9,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.F_FULL[0]", x-4,y+10,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.F_FULL[1]", x-4,y+12,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.F_EMPTY[0]", x-4,y+10,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.F_EMPTY[1]", x-4,y+13,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.F_AL_FULL[0]", x-4,y+11,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.F_AL_FULL[1]", x-4,y+12,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.F_AL_EMPTY[0]", x-4,y+11,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.F_AL_EMPTY[1]", x-4,y+13,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FWR_ERR[0]", x-4,y+4,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FWR_ERR[1]", x-4,y+5,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FRD_ERR[0]", x-4,y+4,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FRD_ERR[1]", x-4,y+5,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FWR_ADDR[0]", x-6,y+8,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FWR_ADDRX[0]", x-5,y+8,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FWR_ADDR[1]", x-6,y+8,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FWR_ADDRX[1]", x-5,y+8,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FWR_ADDR[2]", x-6,y+9,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FWR_ADDRX[2]", x-5,y+9,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FWR_ADDR[3]", x-6,y+9,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FWR_ADDRX[3]", x-5,y+9,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FWR_ADDR[4]", x-6,y+10,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FWR_ADDRX[4]", x-5,y+10,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FWR_ADDR[5]", x-6,y+10,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FWR_ADDRX[5]", x-5,y+10,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FWR_ADDR[6]", x-6,y+11,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FWR_ADDRX[6]", x-5,y+11,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FWR_ADDR[7]", x-6,y+11,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FWR_ADDRX[7]", x-5,y+11,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FWR_ADDR[8]", x-6,y+12,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FWR_ADDRX[8]", x-5,y+12,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FWR_ADDR[9]", x-6,y+12,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FWR_ADDRX[9]", x-5,y+12,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FWR_ADDR[10]", x-6,y+13,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FWR_ADDRX[10]", x-5,y+13,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FWR_ADDR[11]", x-6,y+13,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FWR_ADDRX[11]", x-5,y+13,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FWR_ADDR[12]", x-6,y+14,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FWR_ADDRX[12]", x-5,y+14,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FWR_ADDR[13]", x-6,y+14,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FWR_ADDRX[13]", x-5,y+14,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FWR_ADDR[14]", x-6,y+15,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FWR_ADDRX[14]", x-5,y+15,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FWR_ADDR[15]", x-6,y+15,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FWR_ADDRX[15]", x-5,y+15,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FRD_ADDR[0]", x-6,y+0,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FRD_ADDRX[0]", x-5,y+0,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FRD_ADDR[1]", x-6,y+0,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FRD_ADDRX[1]", x-5,y+0,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FRD_ADDR[2]", x-6,y+1,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FRD_ADDRX[2]", x-5,y+1,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FRD_ADDR[3]", x-6,y+1,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FRD_ADDRX[3]", x-5,y+1,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FRD_ADDR[4]", x-6,y+2,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FRD_ADDRX[4]", x-5,y+2,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FRD_ADDR[5]", x-6,y+2,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FRD_ADDRX[5]", x-5,y+2,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FRD_ADDR[6]", x-6,y+3,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FRD_ADDRX[6]", x-5,y+3,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FRD_ADDR[7]", x-6,y+3,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FRD_ADDRX[7]", x-5,y+3,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FRD_ADDR[8]", x-6,y+4,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FRD_ADDRX[8]", x-5,y+4,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FRD_ADDR[9]", x-6,y+4,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FRD_ADDRX[9]", x-5,y+4,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FRD_ADDR[10]", x-6,y+5,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FRD_ADDRX[10]", x-5,y+5,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FRD_ADDR[11]", x-6,y+5,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FRD_ADDRX[11]", x-5,y+5,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FRD_ADDR[12]", x-6,y+6,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FRD_ADDRX[12]", x-5,y+6,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FRD_ADDR[13]", x-6,y+6,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FRD_ADDRX[13]", x-5,y+6,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FRD_ADDR[14]", x-6,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FRD_ADDRX[14]", x-5,y+7,"CPE.RAM_I1")
        self.create_conn(x,y,"RAM.FRD_ADDR[15]", x-6,y+7,"CPE.RAM_I2")
        self.create_conn(x,y,"RAM.FRD_ADDRX[15]", x-5,y+7,"CPE.RAM_I2")
        if is_ram(x,y-16):
            self.create_conn(x,y,"RAM.FORW_CAS_WRAO", x,y-16,"RAM.FORW_CAS_WRAI")
            self.create_conn(x,y,"RAM.FORW_CAS_WRBO", x,y-16,"RAM.FORW_CAS_WRBI")
            self.create_conn(x,y,"RAM.FORW_CAS_BMAO", x,y-16,"RAM.FORW_CAS_BMAI")
            self.create_conn(x,y,"RAM.FORW_CAS_BMBO", x,y-16,"RAM.FORW_CAS_BMBI")
            self.create_conn(x,y,"RAM.FORW_CAS_RDAO", x,y-16,"RAM.FORW_CAS_RDAI")
            self.create_conn(x,y,"RAM.FORW_CAS_RDBO", x,y-16,"RAM.FORW_CAS_RDBI")
            self.create_conn(x,y,"RAM.FORW_UADDRAO[0]", x,y-16,"RAM.FORW_UADDRAI[0]")
            self.create_conn(x,y,"RAM.FORW_UADDRAO[1]", x,y-16,"RAM.FORW_UADDRAI[1]")
            self.create_conn(x,y,"RAM.FORW_UADDRAO[2]", x,y-16,"RAM.FORW_UADDRAI[2]")
            self.create_conn(x,y,"RAM.FORW_UADDRAO[3]", x,y-16,"RAM.FORW_UADDRAI[3]")
            self.create_conn(x,y,"RAM.FORW_UADDRAO[4]", x,y-16,"RAM.FORW_UADDRAI[4]")
            self.create_conn(x,y,"RAM.FORW_UADDRAO[5]", x,y-16,"RAM.FORW_UADDRAI[5]")
            self.create_conn(x,y,"RAM.FORW_UADDRAO[6]", x,y-16,"RAM.FORW_UADDRAI[6]")
            self.create_conn(x,y,"RAM.FORW_UADDRAO[7]", x,y-16,"RAM.FORW_UADDRAI[7]")
            self.create_conn(x,y,"RAM.FORW_UADDRAO[8]", x,y-16,"RAM.FORW_UADDRAI[8]")
            self.create_conn(x,y,"RAM.FORW_UADDRAO[9]", x,y-16,"RAM.FORW_UADDRAI[9]")
            self.create_conn(x,y,"RAM.FORW_UADDRAO[10]", x,y-16,"RAM.FORW_UADDRAI[10]")
            self.create_conn(x,y,"RAM.FORW_UADDRAO[11]", x,y-16,"RAM.FORW_UADDRAI[11]")
            self.create_conn(x,y,"RAM.FORW_UADDRAO[12]", x,y-16,"RAM.FORW_UADDRAI[12]")
            self.create_conn(x,y,"RAM.FORW_UADDRAO[13]", x,y-16,"RAM.FORW_UADDRAI[13]")
            self.create_conn(x,y,"RAM.FORW_UADDRAO[14]", x,y-16,"RAM.FORW_UADDRAI[14]")
            self.create_conn(x,y,"RAM.FORW_UADDRAO[15]", x,y-16,"RAM.FORW_UADDRAI[15]")
            self.create_conn(x,y,"RAM.FORW_LADDRAO[0]", x,y-16,"RAM.FORW_LADDRAI[0]")
            self.create_conn(x,y,"RAM.FORW_LADDRAO[1]", x,y-16,"RAM.FORW_LADDRAI[1]")
            self.create_conn(x,y,"RAM.FORW_LADDRAO[2]", x,y-16,"RAM.FORW_LADDRAI[2]")
            self.create_conn(x,y,"RAM.FORW_LADDRAO[3]", x,y-16,"RAM.FORW_LADDRAI[3]")
            self.create_conn(x,y,"RAM.FORW_LADDRAO[4]", x,y-16,"RAM.FORW_LADDRAI[4]")
            self.create_conn(x,y,"RAM.FORW_LADDRAO[5]", x,y-16,"RAM.FORW_LADDRAI[5]")
            self.create_conn(x,y,"RAM.FORW_LADDRAO[6]", x,y-16,"RAM.FORW_LADDRAI[6]")
            self.create_conn(x,y,"RAM.FORW_LADDRAO[7]", x,y-16,"RAM.FORW_LADDRAI[7]")
            self.create_conn(x,y,"RAM.FORW_LADDRAO[8]", x,y-16,"RAM.FORW_LADDRAI[8]")
            self.create_conn(x,y,"RAM.FORW_LADDRAO[9]", x,y-16,"RAM.FORW_LADDRAI[9]")
            self.create_conn(x,y,"RAM.FORW_LADDRAO[10]", x,y-16,"RAM.FORW_LADDRAI[10]")
            self.create_conn(x,y,"RAM.FORW_LADDRAO[11]", x,y-16,"RAM.FORW_LADDRAI[11]")
            self.create_conn(x,y,"RAM.FORW_LADDRAO[12]", x,y-16,"RAM.FORW_LADDRAI[12]")
            self.create_conn(x,y,"RAM.FORW_LADDRAO[13]", x,y-16,"RAM.FORW_LADDRAI[13]")
            self.create_conn(x,y,"RAM.FORW_LADDRAO[14]", x,y-16,"RAM.FORW_LADDRAI[14]")
            self.create_conn(x,y,"RAM.FORW_LADDRAO[15]", x,y-16,"RAM.FORW_LADDRAI[15]")
            self.create_conn(x,y,"RAM.FORW_UADDRBO[0]", x,y-16,"RAM.FORW_UADDRBI[0]")
            self.create_conn(x,y,"RAM.FORW_UADDRBO[1]", x,y-16,"RAM.FORW_UADDRBI[1]")
            self.create_conn(x,y,"RAM.FORW_UADDRBO[2]", x,y-16,"RAM.FORW_UADDRBI[2]")
            self.create_conn(x,y,"RAM.FORW_UADDRBO[3]", x,y-16,"RAM.FORW_UADDRBI[3]")
            self.create_conn(x,y,"RAM.FORW_UADDRBO[4]", x,y-16,"RAM.FORW_UADDRBI[4]")
            self.create_conn(x,y,"RAM.FORW_UADDRBO[5]", x,y-16,"RAM.FORW_UADDRBI[5]")
            self.create_conn(x,y,"RAM.FORW_UADDRBO[6]", x,y-16,"RAM.FORW_UADDRBI[6]")
            self.create_conn(x,y,"RAM.FORW_UADDRBO[7]", x,y-16,"RAM.FORW_UADDRBI[7]")
            self.create_conn(x,y,"RAM.FORW_UADDRBO[8]", x,y-16,"RAM.FORW_UADDRBI[8]")
            self.create_conn(x,y,"RAM.FORW_UADDRBO[9]", x,y-16,"RAM.FORW_UADDRBI[9]")
            self.create_conn(x,y,"RAM.FORW_UADDRBO[10]", x,y-16,"RAM.FORW_UADDRBI[10]")
            self.create_conn(x,y,"RAM.FORW_UADDRBO[11]", x,y-16,"RAM.FORW_UADDRBI[11]")
            self.create_conn(x,y,"RAM.FORW_UADDRBO[12]", x,y-16,"RAM.FORW_UADDRBI[12]")
            self.create_conn(x,y,"RAM.FORW_UADDRBO[13]", x,y-16,"RAM.FORW_UADDRBI[13]")
            self.create_conn(x,y,"RAM.FORW_UADDRBO[14]", x,y-16,"RAM.FORW_UADDRBI[14]")
            self.create_conn(x,y,"RAM.FORW_UADDRBO[15]", x,y-16,"RAM.FORW_UADDRBI[15]")
            self.create_conn(x,y,"RAM.FORW_LADDRBO[0]", x,y-16,"RAM.FORW_LADDRBI[0]")
            self.create_conn(x,y,"RAM.FORW_LADDRBO[1]", x,y-16,"RAM.FORW_LADDRBI[1]")
            self.create_conn(x,y,"RAM.FORW_LADDRBO[2]", x,y-16,"RAM.FORW_LADDRBI[2]")
            self.create_conn(x,y,"RAM.FORW_LADDRBO[3]", x,y-16,"RAM.FORW_LADDRBI[3]")
            self.create_conn(x,y,"RAM.FORW_LADDRBO[4]", x,y-16,"RAM.FORW_LADDRBI[4]")
            self.create_conn(x,y,"RAM.FORW_LADDRBO[5]", x,y-16,"RAM.FORW_LADDRBI[5]")
            self.create_conn(x,y,"RAM.FORW_LADDRBO[6]", x,y-16,"RAM.FORW_LADDRBI[6]")
            self.create_conn(x,y,"RAM.FORW_LADDRBO[7]", x,y-16,"RAM.FORW_LADDRBI[7]")
            self.create_conn(x,y,"RAM.FORW_LADDRBO[8]", x,y-16,"RAM.FORW_LADDRBI[8]")
            self.create_conn(x,y,"RAM.FORW_LADDRBO[9]", x,y-16,"RAM.FORW_LADDRBI[9]")
            self.create_conn(x,y,"RAM.FORW_LADDRBO[10]", x,y-16,"RAM.FORW_LADDRBI[10]")
            self.create_conn(x,y,"RAM.FORW_LADDRBO[11]", x,y-16,"RAM.FORW_LADDRBI[11]")
            self.create_conn(x,y,"RAM.FORW_LADDRBO[12]", x,y-16,"RAM.FORW_LADDRBI[12]")
            self.create_conn(x,y,"RAM.FORW_LADDRBO[13]", x,y-16,"RAM.FORW_LADDRBI[13]")
            self.create_conn(x,y,"RAM.FORW_LADDRBO[14]", x,y-16,"RAM.FORW_LADDRBI[14]")
            self.create_conn(x,y,"RAM.FORW_LADDRBO[15]", x,y-16,"RAM.FORW_LADDRBI[15]")
            self.create_conn(x,y,"RAM.FORW_UA0CLKO", x,y-16,"RAM.FORW_UA0CLKI")
            self.create_conn(x,y,"RAM.FORW_UA0ENO", x,y-16,"RAM.FORW_UA0ENI")
            self.create_conn(x,y,"RAM.FORW_UA0WEO", x,y-16,"RAM.FORW_UA0WEI")
            self.create_conn(x,y,"RAM.FORW_LA0CLKO", x,y-16,"RAM.FORW_LA0CLKI")
            self.create_conn(x,y,"RAM.FORW_LA0ENO", x,y-16,"RAM.FORW_LA0ENI")
            self.create_conn(x,y,"RAM.FORW_LA0WEO", x,y-16,"RAM.FORW_LA0WEI")
            self.create_conn(x,y,"RAM.FORW_UA1CLKO", x,y-16,"RAM.FORW_UA1CLKI")
            self.create_conn(x,y,"RAM.FORW_UA1ENO", x,y-16,"RAM.FORW_UA1ENI")
            self.create_conn(x,y,"RAM.FORW_UA1WEO", x,y-16,"RAM.FORW_UA1WEI")
            self.create_conn(x,y,"RAM.FORW_LA1CLKO", x,y-16,"RAM.FORW_LA1CLKI")
            self.create_conn(x,y,"RAM.FORW_LA1ENO", x,y-16,"RAM.FORW_LA1ENI")
            self.create_conn(x,y,"RAM.FORW_LA1WEO", x,y-16,"RAM.FORW_LA1WEI")
            self.create_conn(x,y,"RAM.FORW_UB0CLKO", x,y-16,"RAM.FORW_UB0CLKI")
            self.create_conn(x,y,"RAM.FORW_UB0ENO", x,y-16,"RAM.FORW_UB0ENI")
            self.create_conn(x,y,"RAM.FORW_UB0WEO", x,y-16,"RAM.FORW_UB0WEI")
            self.create_conn(x,y,"RAM.FORW_LB0CLKO", x,y-16,"RAM.FORW_LB0CLKI")
            self.create_conn(x,y,"RAM.FORW_LB0ENO", x,y-16,"RAM.FORW_LB0ENI")
            self.create_conn(x,y,"RAM.FORW_LB0WEO", x,y-16,"RAM.FORW_LB0WEI")
            self.create_conn(x,y,"RAM.FORW_UB1CLKO", x,y-16,"RAM.FORW_UB1CLKI")
            self.create_conn(x,y,"RAM.FORW_UB1ENO", x,y-16,"RAM.FORW_UB1ENI")
            self.create_conn(x,y,"RAM.FORW_UB1WEO", x,y-16,"RAM.FORW_UB1WEI")
            self.create_conn(x,y,"RAM.FORW_LB1CLKO", x,y-16,"RAM.FORW_LB1CLKI")
            self.create_conn(x,y,"RAM.FORW_LB1ENO", x,y-16,"RAM.FORW_LB1ENI")
            self.create_conn(x,y,"RAM.FORW_LB1WEO", x,y-16,"RAM.FORW_LB1WEI")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB0", x, y, "RAM.CLOCK1")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB1", x, y, "RAM.CLOCK2")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB2", x, y, "RAM.CLOCK3")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB3", x, y, "RAM.CLOCK4")

    def create_in_die_connections(self, conn):
        self.conn = conn
        for y in range(-2, max_row()+1):
            for x in range(-2, max_col()+1):
                if is_cpe(x,y):
                    self.create_cpe(x,y)
                    self.create_inmux(x,y)
                    if is_outmux(x,y):
                        self.create_outmux(x,y)
                if is_sb(x,y):
                    self.create_sb(x,y)
                if is_edge_io(x,y):
                    self.create_io(x,y)
                if is_ram(x,y):
                    self.create_ram(x,y)
                if is_serdes(x,y):
                    self.create_serdes(x,y)
        self.create_pll()
        self.global_mesh()
        self.edge_select()
        self.misc_connections()
