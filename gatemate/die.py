from enum import Enum

def max_row():
    return 131

def max_col():
    return 163

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
    return x==-2 and y>=1 and y<=130

def is_edge_right(x,y):
    return x==max_col() and y>=1 and y<=128

def is_edge_bottom(x,y):
    return y==-2 and x>=-1 and x<=162

def is_edge_top(x,y):
    return y==max_row() and x>=1 and x<=162

def is_edge_io(x,y):
    if (y==-2 and x>=5 and x<=40): # GPIO_S3
        return True
    if (y==-2 and x>=57 and x<=92):  # GPIO_S1
        return True
    if (y==-2 and x>=101 and x<=136): # GPIO_S2
        return True
    if (x==-2 and y>=25 and y<=60): # GPIO_W1
        return True
    if (x==-2 and y>=69 and y<=104): # GPIO_W2
        return True
    if (x==max_col() and y>=25 and y<=50): # GPIO_E1
        return True
    if (x==max_col() and y>=69 and y<=104): # GPIO_E2
        return True
    if (y==max_row() and x>=57 and x<=92): # GPIO_N1
        return True
    if (y==max_row() and x>=101 and x<=136): # GPIO_N2
        return True

def is_gpio(x,y):
    if is_edge_io(x,y):
        if (y==-2 or y==max_row()):
            return x % 2==1
        if (x==-2 or x==max_col()):
            return y % 2==1
    return False

class PinType(Enum):
    INPUT = 0
    OUTPUT = 1
    INOUT = 2

PRIMITIVES_PINS = {
    "CPE": {
        "RAM_I1" : [ PinType.INPUT,  "CPE_WIRE_L" ],
        "RAM_I2" : [ PinType.INPUT,  "CPE_WIRE_L" ],
        "IN1"    : [ PinType.INPUT,  "CPE_WIRE_L" ],
        "IN2"    : [ PinType.INPUT,  "CPE_WIRE_L" ],
        "IN3"    : [ PinType.INPUT,  "CPE_WIRE_L" ],
        "IN4"    : [ PinType.INPUT,  "CPE_WIRE_L" ],
        "IN5"    : [ PinType.INPUT,  "CPE_WIRE_L" ],
        "IN6"    : [ PinType.INPUT,  "CPE_WIRE_L" ],
        "IN7"    : [ PinType.INPUT,  "CPE_WIRE_L" ],
        "IN8"    : [ PinType.INPUT,  "CPE_WIRE_L" ],
        "CLK"    : [ PinType.INPUT,  "CPE_WIRE_L" ],
        "EN"     : [ PinType.INPUT,  "CPE_WIRE_L" ],
        "SR"     : [ PinType.INPUT,  "CPE_WIRE_L" ],
        "CINX"   : [ PinType.INPUT,  "CPE_WIRE_L" ],
        "PINX"   : [ PinType.INPUT,  "CPE_WIRE_L" ],
        "CINY1"  : [ PinType.INPUT,  "CPE_WIRE_B" ],
        "PINY1"  : [ PinType.INPUT,  "CPE_WIRE_B" ],
        "CINY2"  : [ PinType.INPUT,  "CPE_WIRE_B" ],
        "PINY2"  : [ PinType.INPUT,  "CPE_WIRE_B" ],
        "OUT1"   : [ PinType.OUTPUT, "CPE_WIRE_B" ],
        "OUT2"   : [ PinType.OUTPUT, "CPE_WIRE_B" ],        
        "RAM_O1" : [ PinType.OUTPUT, "CPE_WIRE_B" ],
        "RAM_O2" : [ PinType.OUTPUT, "CPE_WIRE_B" ],
        "COUTX"  : [ PinType.OUTPUT, "CPE_WIRE_B" ],
        "POUTX"  : [ PinType.OUTPUT, "CPE_WIRE_B" ],
        "COUTY1" : [ PinType.OUTPUT, "CPE_WIRE_T" ],
        "POUTY1" : [ PinType.OUTPUT, "CPE_WIRE_T" ],
        "COUTY2" : [ PinType.OUTPUT, "CPE_WIRE_T" ],
        "POUTY2" : [ PinType.OUTPUT, "CPE_WIRE_T" ],
    },
    "GPIO" : {
        "IN1"    : [ PinType.OUTPUT, "GPIO_WIRE" ],
        "IN2"    : [ PinType.OUTPUT, "GPIO_WIRE" ],
        "OUT1"   : [ PinType.INPUT,  "GPIO_WIRE" ],
        "OUT2"   : [ PinType.INPUT,  "GPIO_WIRE" ],
        "OUT3"   : [ PinType.INPUT,  "GPIO_WIRE" ],
        "OUT4"   : [ PinType.INPUT,  "GPIO_WIRE" ],
        "DDR"    : [ PinType.INPUT,  "GPIO_WIRE" ],
        "RESET"  : [ PinType.INPUT,  "GPIO_WIRE" ],
        "CLOCK1" : [ PinType.INPUT,  "GPIO_WIRE" ],
        "CLOCK2" : [ PinType.INPUT,  "GPIO_WIRE" ],
        "CLOCK3" : [ PinType.INPUT,  "GPIO_WIRE" ],
        "CLOCK4" : [ PinType.INPUT,  "GPIO_WIRE" ],
    }
}

def get_groups_for_type(type):
    groups = []
    def create_group(name, type):
        groups.append({"name":name, "type":type})
    if "CPE" in type:
        # CPE
        for p in range(1,13):
            create_group(f"INMUX_P{p:02d}", "INMUX")
            if "OUTMUX" in type and p>=9:
                create_group(f"OUTMUX_P{p:02d}", "OUTMUX")
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
    #if "EDGE_IO" in type:
    #    # EDGE_IO
    return groups

def get_bels_for_type(type):
    bels = []
    if "CPE" in type:
        bels.append({"name":"CPE", "type":"CPE", "z":0})
    if "GPIO" in type:
        bels.append({"name":"GPIO", "type":"GPIO", "z":0})
    return bels

def get_bel_pins(bel):
    return PRIMITIVES_PINS[bel].items()

def get_endpoints_for_type(type):
    wires = []
    def create_wire(name, type):
        wires.append({"name":name, "type":type})

    for bel in get_bels_for_type(type):
        for k,v in get_bel_pins(bel["type"]):
            create_wire(f"{bel["name"]}.{k}", type=f"{v[1]}")

    if "CPE" in type:
        # CPE
        for p in range(1,13):
            plane = f"{p:02d}"
            for i in range(8):
                create_wire(f"INMUX.P{plane}.D{i}", type="INMUX_WIRE")
            create_wire(f"INMUX.P{plane}.Y", type="INMUX_WIRE")
            if "OUTMUX" in type and p>=9:
                for i in range(4):
                    create_wire(f"OUTMUX.P{plane}.D{i}", type="OUTMUX_WIRE")
                create_wire(f"OUTMUX.P{plane}.Y", type="OUTMUX_WIRE")

    if "SB_BIG" in type:
        # SB_BIG
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

    if "SB_SML" in type:
        # SB_SML
        for p in range(1,13):
            plane = f"{p:02d}"
            create_wire(f"SB_SML.P{plane}.D0", type="SB_SML_WIRE")
            for i in range(1,5):
                create_wire(f"SB_SML.P{plane}.D2_{i}", type="SB_SML_WIRE")
                create_wire(f"SB_SML.P{plane}.D3_{i}", type="SB_SML_WIRE")
                create_wire(f"SB_SML.P{plane}.Y{i}", type="SB_SML_WIRE")

            create_wire(f"SB_SML.P{plane}.YDIAG", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.X34", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.X14", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.X12", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.X23", type="SB_SML_WIRE")
    #if "GPIO" in type:
        # GPIO
    #if "EDGE_IO" in type:
    #    # EDGE_IO
    return wires

def get_mux_connections_for_type(type):
    muxes = []
    def create_mux(src, dst, bits, value):
        mux = dst.replace(".","_") + "_MUX"
        muxes.append({"src":src, "dst":dst, "mux":mux, "bits":bits, "value": value})

    if "CPE" in type:
        # CPE
        for p in range(1,13):
            plane = f"{p:02d}"
            for i in range(8):
                create_mux(f"INMUX.P{plane}.D{i}", f"INMUX.P{plane}.Y", 3, i)
            if "OUTMUX" in type and p>=9:
                for i in range(4):
                    create_mux(f"OUTMUX.P{plane}.D{i}", f"OUTMUX.P{plane}.Y", 2, i)

    if "SB_BIG" in type:
        # SB_BIG
        for p in range(1,13):
            plane = f"{p:02d}"
            # Per Y output mux
            for i in range(1,5):
                create_mux(f"SB_BIG.P{plane}.D0",     f"SB_BIG.P{plane}.Y{i}", 3, 0)
                create_mux(f"SB_BIG.P{plane}.YDIAG",  f"SB_BIG.P{plane}.Y{i}", 3, 1)
                create_mux(f"SB_BIG.P{plane}.D2_{i}", f"SB_BIG.P{plane}.Y{i}", 3, 2)
                create_mux(f"SB_BIG.P{plane}.D3_{i}", f"SB_BIG.P{plane}.Y{i}", 3, 3)
                create_mux(f"SB_BIG.P{plane}.D4_{i}", f"SB_BIG.P{plane}.Y{i}", 3, 4)
                create_mux(f"SB_BIG.P{plane}.D5_{i}", f"SB_BIG.P{plane}.Y{i}", 3, 5)
                create_mux(f"SB_BIG.P{plane}.D6_{i}", f"SB_BIG.P{plane}.Y{i}", 3, 6)
                create_mux(f"SB_BIG.P{plane}.D7_{i}", f"SB_BIG.P{plane}.Y{i}", 3, 7)

            # YDIAG output mux
            create_mux(f"SB_BIG.P{plane}.Y1",  f"SB_BIG.P{plane}.YDIAG", 3, 0)
            create_mux(f"SB_BIG.P{plane}.Y2",  f"SB_BIG.P{plane}.YDIAG", 3, 1)
            create_mux(f"SB_BIG.P{plane}.Y3",  f"SB_BIG.P{plane}.YDIAG", 3, 2)
            create_mux(f"SB_BIG.P{plane}.Y4",  f"SB_BIG.P{plane}.YDIAG", 3, 3)
            create_mux(f"SB_BIG.P{plane}.X34", f"SB_BIG.P{plane}.YDIAG", 3, 4)
            create_mux(f"SB_BIG.P{plane}.X14", f"SB_BIG.P{plane}.YDIAG", 3, 5)
            create_mux(f"SB_BIG.P{plane}.X12", f"SB_BIG.P{plane}.YDIAG", 3, 6)
            create_mux(f"SB_BIG.P{plane}.X23", f"SB_BIG.P{plane}.YDIAG", 3, 7)
    if "SB_SML" in type:
        # SB_SML
        for p in range(1,13):
            plane = f"{p:02d}"
            # Per Y output mux
            for i in range(1,5):
                create_mux(f"SB_SML.P{plane}.D0",     f"SB_SML.P{plane}.Y{i}", 2, 0)
                create_mux(f"SB_SML.P{plane}.YDIAG",  f"SB_SML.P{plane}.Y{i}", 2, 1)
                create_mux(f"SB_SML.P{plane}.D2_{i}", f"SB_SML.P{plane}.Y{i}", 2, 2)
                create_mux(f"SB_SML.P{plane}.D3_{i}", f"SB_SML.P{plane}.Y{i}", 2, 3)

            # YDIAG output mux
            create_mux(f"SB_SML.P{plane}.Y1",  f"SB_SML.P{plane}.YDIAG", 3, 0)
            create_mux(f"SB_SML.P{plane}.Y2",  f"SB_SML.P{plane}.YDIAG", 3, 1)
            create_mux(f"SB_SML.P{plane}.Y3",  f"SB_SML.P{plane}.YDIAG", 3, 2)
            create_mux(f"SB_SML.P{plane}.Y4",  f"SB_SML.P{plane}.YDIAG", 3, 3)
            create_mux(f"SB_SML.P{plane}.X34", f"SB_SML.P{plane}.YDIAG", 3, 4)
            create_mux(f"SB_SML.P{plane}.X14", f"SB_SML.P{plane}.YDIAG", 3, 5)
            create_mux(f"SB_SML.P{plane}.X12", f"SB_SML.P{plane}.YDIAG", 3, 6)
            create_mux(f"SB_SML.P{plane}.X23", f"SB_SML.P{plane}.YDIAG", 3, 7)

    #if "GPIO" in type:
    #    # GPIO
    #if "EDGE_IO" in type:
    #    # EDGE_IO
    return muxes

def get_tile_type(x,y):
    val = list()
    if is_cpe(x,y):
        val.append("CPE")
        if is_outmux(x,y): 
            val.append("OUTMUX")

    if is_sb_big(x,y):
        val.append("SB_BIG")
    if is_sb_sml(x,y):
        val.append("SB_SML")
    if is_gpio(x,y):
        val.append("GPIO")
    if is_edge_io(x,y):
        val.append("EDGE_IO")
    if is_edge_top(x,y):        
        val.append("TOP")
    if is_edge_bottom(x,y):
        val.append("BOTTOM")
    if is_edge_left(x,y):
        val.append("LEFT")
    if is_edge_right(x,y):
        val.append("RIGHT")

    if not val:
        val.append("NONE")
    return "_".join(val)

def get_tile_type_list():    
    tt = set()
    for y in range(-2, max_row()+1):
        for x in range(-2, max_col()+1):
            tt.add(get_tile_type(x,y))

    return tt

conn = dict()
debug_conn = False

def create_conn(src_x,src_y, src, dst_x, dst_y, dst):
    key_val = f"{src_x}/{src_y}/{src}"
    key = { "x" : src_x, "y" : src_y, "w" : src }
    item = { "x" : dst_x,"y" : dst_y, "w" : dst }
    if key_val not in conn:
        conn[key_val] = list()
        conn[key_val].append(key)
    conn[key_val].append(item)
    if debug_conn:
        print(f"({src_x},{src_y}) {src} => ({dst_x},{dst_y}) {dst}")


def alt_plane(dir,plane):
    alt = [[5, 6, 7, 8, 1, 2, 3, 4,11,12, 9,10],
           [9,10,11,12, 9,10,11,12,12,11,10, 9]]
    return alt[dir][plane-1]

def create_cpe(x,y):
    create_conn(x,y,"INMUX.P01.Y", x,y,"CPE.IN1")
    create_conn(x,y,"INMUX.P02.Y", x,y,"CPE.IN2")
    create_conn(x,y,"INMUX.P03.Y", x,y,"CPE.IN3")
    create_conn(x,y,"INMUX.P04.Y", x,y,"CPE.IN4")
    create_conn(x,y,"INMUX.P05.Y", x,y,"CPE.IN5")
    create_conn(x,y,"INMUX.P06.Y", x,y,"CPE.IN6")
    create_conn(x,y,"INMUX.P07.Y", x,y,"CPE.IN7")
    create_conn(x,y,"INMUX.P08.Y", x,y,"CPE.IN8")
    create_conn(x,y,"INMUX.P09.Y", x,y,"CPE.CLK")
    create_conn(x,y,"INMUX.P10.Y", x,y,"CPE.EN")
    create_conn(x,y,"INMUX.P11.Y", x,y,"CPE.SR")
    if is_cpe(x,y-1):
        create_conn(x,y-1,"CPE.COUTY1", x,y,"CPE.CINY1")
        create_conn(x,y-1,"CPE.COUTY2", x,y,"CPE.CINY2")
        create_conn(x,y-1,"CPE.POUTY1", x,y,"CPE.PINY1")
        create_conn(x,y-1,"CPE.POUTY2", x,y,"CPE.PINY2")
    if is_cpe(x-1,y):
        create_conn(x-1,y,"CPE.COUTX", x,y,"CPE.CINX")
        create_conn(x-1,y,"CPE.POUTX", x,y,"CPE.PINX")

def create_inmux(x,y):
    for p in range(1,13):
        plane = f"{p:02d}"

        # D0 - D3 are from nearby SBs
        offset = 2 if is_sb(x,y) else 1
        create_conn(x-offset,y,f"{get_sb_type(x-offset,y)}.P{plane}.Y1", x,y,f"INMUX.P{plane}.D0")
        create_conn(x,y-offset,f"{get_sb_type(x,y-offset)}.P{plane}.Y2", x,y,f"INMUX.P{plane}.D1")
        create_conn(x+offset,y,f"{get_sb_type(x+offset,y)}.P{plane}.Y3", x,y,f"INMUX.P{plane}.D2")
        create_conn(x,y+offset,f"{get_sb_type(x,y+offset)}.P{plane}.Y4", x,y,f"INMUX.P{plane}.D3")

        # D4 and D5 are from diagonal INMUX
        if is_cpe(x-1,y-1):
            create_conn(x-1,y-1,f"INMUX.P{plane}.Y", x,y,f"INMUX.P{plane}.D4")
        if is_cpe(x+1,y+1):
            create_conn(x+1,y+1,f"INMUX.P{plane}.Y", x,y,f"INMUX.P{plane}.D5")

        # D6 and D7 are from alternate planes
        alt = f"{alt_plane(0,p):02d}"
        create_conn(x,y,f"INMUX.P{alt}.Y", x,y,f"INMUX.P{plane}.D6")
        alt = f"{alt_plane(1,p):02d}"
        create_conn(x,y,f"INMUX.P{alt}.Y", x,y,f"INMUX.P{plane}.D7")

OUT_PLANE_1 = [ 2, 1, 2, 1, 1, 2, 1, 2]
OUT_PLANE_2 = [ 1, 2, 1, 2, 2, 1, 2, 1]

def create_sb(x,y):
    block_x = ((x-1) & ~1) + 1
    block_y = ((y-1) & ~1) + 1
    sb_type = get_sb_type(x,y)

    for p in range(1,13):
        plane = f"{p:02d}"
        # Handling input D0
        if is_cpe(x,y):
            # Core section SBs are connected to CPE
            if (p<9):
                # planes 1..8
                # for SB in lower left section of block
                #   x offset +0 y offset +0 output 2 plane 1
                #   x offset +0 y offset +1 output 1 plane 2
                #   x offset +1 y offset +0 output 2 plane 3
                #   x offset +1 y offset +1 output 1 plane 4
                #   x offset +0 y offset +0 output 1 plane 5
                #   x offset +0 y offset +1 output 2 plane 6
                #   x offset +1 y offset +0 output 1 plane 7
                #   x offset +1 y offset +1 output 2 plane 8
                # for SB in upper right section of block
                # difference is only that outputs are reversed
                x_cpe = block_x + (1 if (p-1) & 2 else 0)
                y_cpe = block_y + (1 if (p-1) & 1 else 0)
                out = OUT_PLANE_1[p-1] if x & 1 else OUT_PLANE_2[p-1]
                create_conn(x_cpe,y_cpe,f"CPE.OUT{out}", x,y,f"{sb_type}.P{plane}.D0")
            else:
                # planes 9..12
                create_conn(x,y,f"OUTMUX.P{plane}.Y", x,y,f"{sb_type}.P{plane}.D0")
#        else:
            # Handling GPIO connections
        # Handling other inputs
        

def create_outmux(x,y):
    block_x = ((x-1) & ~1) + 1
    block_y = ((y-1) & ~1) + 1
    for p in range(9,13):
        plane = f"{p:02d}"
        output_1 = 1 if (x % 2)  ^ (p % 2) else 2
        output_2 = 2 if (x % 2)  ^ (p % 2) else 1
        create_conn(block_x,   block_y,   f"CPE.OUT{output_1}", x,y, f"OUTMUX.P{plane}.D0")
        create_conn(block_x,   block_y+1, f"CPE.OUT{output_1}", x,y, f"OUTMUX.P{plane}.D1")
        create_conn(block_x+1, block_y,   f"CPE.OUT{output_2}", x,y, f"OUTMUX.P{plane}.D2")
        create_conn(block_x+1, block_y+1, f"CPE.OUT{output_2}", x,y, f"OUTMUX.P{plane}.D3")

def get_connections():
    for y in range(-2, max_row()+1):
        for x in range(-2, max_col()+1):
            if is_cpe(x,y):
                create_cpe(x,y)
                create_inmux(x,y)
                if is_outmux(x,y):
                    create_outmux(x,y)
            if is_sb(x,y):
                create_sb(x,y)
    return conn.items()
