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
    return not(x<=0 or x>=160 or y<=0 or y>=120)

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

def get_tile_type_list():
    return [ "CPE_BIG", "CPE_SML", "CPE",
             "SB_BIG", "SB_SML",
             "GPIO_T", "EDGE_IO_T", "EDGE_T",
             "GPIO_B", "EDGE_IO_B", "EDGE_B",
             "GPIO_L", "EDGE_IO_L", "EDGE_L",
             "GPIO_R", "EDGE_IO_R", "EDGE_R",
             "NONE" ]

class PinType(Enum):
    INPUT = 0
    OUTPUT = 1
    INOUT = 2


CPE_PINS = {
    "RAM_I1" : PinType.INPUT,
    "RAM_I2" : PinType.INPUT,
    "IN1" : PinType.INPUT,
    "IN2" : PinType.INPUT,
    "IN3" : PinType.INPUT,
    "IN4" : PinType.INPUT,
    "IN5" : PinType.INPUT,
    "IN6" : PinType.INPUT,
    "IN7" : PinType.INPUT,
    "IN8" : PinType.INPUT,
    "CLK" : PinType.INPUT,
    "EN" : PinType.INPUT,
    "SR" : PinType.INPUT,
    "CINX" : PinType.INPUT,
    "PINX" : PinType.INPUT,
    "CINY1" : PinType.INPUT,
    "PINY1" : PinType.INPUT,
    "CINY2" : PinType.INPUT,
    "PINY2" : PinType.INPUT,
    "OUT1" : PinType.OUTPUT,
    "OUT2" : PinType.OUTPUT,
    "RAM_O1" : PinType.OUTPUT,
    "RAM_O2" : PinType.OUTPUT,
    "COUTX" : PinType.OUTPUT,
    "POUTX" : PinType.OUTPUT,
    "COUTY1" : PinType.OUTPUT,
    "POUTY1" : PinType.OUTPUT,
    "COUTY2" : PinType.OUTPUT,
    "POUTY2" : PinType.OUTPUT
}

GPIO_PINS = {
    "IN1" : PinType.OUTPUT,
    "IN2" : PinType.OUTPUT,
    "OUT1" : PinType.INPUT,
    "OUT2" : PinType.INPUT,
    "OUT3" : PinType.INPUT,
    "OUT4" : PinType.INPUT,
    "DDR" : PinType.INPUT,
    "RESET" : PinType.INPUT,
    "CLOCK1" : PinType.INPUT,
    "CLOCK2" : PinType.INPUT,
    "CLOCK3" : PinType.INPUT,
    "CLOCK4" : PinType.INPUT,
}

def get_groups_for_type(type):
    groups = []
    def create_group(name, type):
        groups.append({"name":name, "type":type})
    if type.startswith("CPE"):
        # CPE
        for p in range(12):
            create_group(f"INMUX_P{p+1:02d}", "INMUX")
            if "_" in type and p>7: # OUTMUX only on CPE_BIG and CPE_SML
                create_group(f"OUTMUX_P{p+1:02d}", "OUTMUX")
    if "BIG" in type:
        # SB_BIG
        for p in range(12):
            create_group(f"SB_BIG_P{p+1:02d}", "SB_BIG")
    if "SML" in type:
        # SB_SML
        for p in range(12):
            create_group(f"SB_SML_P{p+1:02d}", "SB_SML")
    #if "GPIO" in type:
    #    # GPIO
    #if "EDGE_IO" in type:
    #    # EDGE_IO
    return groups

def get_bels_for_type(type):
    if type.startswith("CPE"):
        return [{"name":"CPE", "type":"CPE", "z":0}]
    if "GPIO" in type:
        return [{"name":"GPIO", "type":"GPIO", "z":0}]
    return []

def get_bel_pins(bel):
    if bel == "CPE":
        return CPE_PINS.items()
    elif bel == "GPIO":
        return GPIO_PINS.items()
    return []


def get_endpoints_for_type(type):
    wires = []
    def create_wire(name, type):
        wires.append({"name":name, "type":type})
    if type.startswith("CPE"):
        # CPE
        create_wire("CPE.IN1", type="CPE_WIRE_L")
        create_wire("CPE.IN2", type="CPE_WIRE_L")
        create_wire("CPE.IN3", type="CPE_WIRE_L")
        create_wire("CPE.IN4", type="CPE_WIRE_L")
        create_wire("CPE.IN5", type="CPE_WIRE_L")
        create_wire("CPE.IN6", type="CPE_WIRE_L")
        create_wire("CPE.IN7", type="CPE_WIRE_L")
        create_wire("CPE.IN8", type="CPE_WIRE_L")
        create_wire("CPE.CLK", type="CPE_WIRE_L")
        create_wire("CPE.EN", type="CPE_WIRE_L")
        create_wire("CPE.SR", type="CPE_WIRE_L")

        create_wire("CPE.RAM_I2", type="CPE_WIRE_L")
        create_wire("CPE.RAM_I1", type="CPE_WIRE_L")
        create_wire("CPE.CINX", type="CPE_WIRE_L")
        create_wire("CPE.PINX", type="CPE_WIRE_L")

        create_wire("CPE.CINY1", type="CPE_WIRE_B")
        create_wire("CPE.PINY1", type="CPE_WIRE_B")
        create_wire("CPE.CINY2", type="CPE_WIRE_B")
        create_wire("CPE.PINY2", type="CPE_WIRE_B")

        create_wire("CPE.OUT2", type="CPE_WIRE_R")
        create_wire("CPE.OUT1", type="CPE_WIRE_R")
        
        create_wire("CPE.RAM_O2", type="CPE_WIRE_R")
        create_wire("CPE.RAM_O1", type="CPE_WIRE_R")
        create_wire("CPE.COUTX", type="CPE_WIRE_R")
        create_wire("CPE.POUTX", type="CPE_WIRE_R")

        create_wire("CPE.COUTY1", type="CPE_WIRE_T")
        create_wire("CPE.POUTY1", type="CPE_WIRE_T")
        create_wire("CPE.COUTY2", type="CPE_WIRE_T")
        create_wire("CPE.POUTY2", type="CPE_WIRE_T")

        for p in range(12):
            plane = f"{p+1:02d}"
            for i in range(8):
                create_wire(f"INMUX.P{plane}.D{i}", type="INMUX_WIRE")
            create_wire(f"INMUX.P{plane}.Y", type="INMUX_WIRE")
            if "_" in type and p>7: # OUTMUX only on CPE_BIG and CPE_SML
                for i in range(4):
                    create_wire(f"OUTMUX.P{plane}.D{i}", type="OUTMUX_WIRE")
                create_wire(f"OUTMUX.P{plane}.Y", type="OUTMUX_WIRE")

    if "BIG" in type:
        # SB_BIG
        for p in range(12):
            plane = f"{p+1:02d}"
            create_wire(f"SB_BIG.P{plane}.D0", type="SB_BIG_WIRE")
            for i in range(4):
                create_wire(f"SB_BIG.P{plane}.D2_{i+1}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.D3_{i+1}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.D4_{i+1}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.D5_{i+1}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.D6_{i+1}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.D7_{i+1}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.Y{i+1}", type="SB_BIG_WIRE")

            create_wire(f"SB_BIG.P{plane}.YDIAG", type="SB_BIG_WIRE")
            create_wire(f"SB_BIG.P{plane}.X34", type="SB_BIG_WIRE")
            create_wire(f"SB_BIG.P{plane}.X14", type="SB_BIG_WIRE")
            create_wire(f"SB_BIG.P{plane}.X12", type="SB_BIG_WIRE")
            create_wire(f"SB_BIG.P{plane}.X23", type="SB_BIG_WIRE")

    if "SML" in type:
        # SB_SML
        for p in range(12):
            plane = f"{p+1:02d}"
            create_wire(f"SB_SML.P{plane}.D0", type="SB_SML_WIRE")
            for i in range(4):
                create_wire(f"SB_SML.P{plane}.D2_{i+1}", type="SB_SML_WIRE")
                create_wire(f"SB_SML.P{plane}.D3_{i+1}", type="SB_SML_WIRE")
                create_wire(f"SB_SML.P{plane}.Y{i+1}", type="SB_SML_WIRE")

            create_wire(f"SB_SML.P{plane}.YDIAG", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.X34", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.X14", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.X12", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.X23", type="SB_SML_WIRE")
    if "GPIO" in type:
        # GPIO
        create_wire("GPIO.IN1", type="GPIO_WIRE")
        create_wire("GPIO.IN2", type="GPIO_WIRE")
        create_wire("GPIO.OUT1", type="GPIO_WIRE")
        create_wire("GPIO.OUT2", type="GPIO_WIRE")
        create_wire("GPIO.OUT3", type="GPIO_WIRE")
        create_wire("GPIO.OUT4", type="GPIO_WIRE")
        create_wire("GPIO.DDR", type="GPIO_WIRE")
        create_wire("GPIO.RESET", type="GPIO_WIRE")
        create_wire("GPIO.CLOCK1", type="GPIO_WIRE")
        create_wire("GPIO.CLOCK2", type="GPIO_WIRE")
        create_wire("GPIO.CLOCK3", type="GPIO_WIRE")
        create_wire("GPIO.CLOCK4", type="GPIO_WIRE")

    #if "EDGE_IO" in type:
    #    # EDGE_IO
    return wires

def get_mux_connections_for_type(type):
    muxes = []
    def create_mux(src, dst, bits, value):
        mux = dst.replace(".","_") + "_MUX"
        muxes.append({"src":src, "dst":dst, "mux":mux, "bits":bits, "value": value})

    if type.startswith("CPE"):
        # CPE
        for p in range(12):
            plane = f"{p+1:02d}"
            for i in range(8):
                create_mux(f"INMUX.P{plane}.D{i}", f"INMUX.P{plane}.Y", 3, i)
            if "_" in type and p>7: # OUTMUX only on CPE_BIG and CPE_SML
                for i in range(4):
                    create_mux(f"OUTMUX.P{plane}.D{i}", f"OUTMUX.P{plane}.Y", 2, i)

    if "BIG" in type:
        # SB_BIG
        for p in range(12):
            plane = f"{p+1:02d}"
            # Per Y output mux
            for i in range(4):
                create_mux(f"SB_BIG.P{plane}.D0",       f"SB_BIG.P{plane}.Y{i+1}", 3, 0)
                create_mux(f"SB_BIG.P{plane}.YDIAG",    f"SB_BIG.P{plane}.Y{i+1}", 3, 1)
                create_mux(f"SB_BIG.P{plane}.D2_{i+1}", f"SB_BIG.P{plane}.Y{i+1}", 3, 2)
                create_mux(f"SB_BIG.P{plane}.D3_{i+1}", f"SB_BIG.P{plane}.Y{i+1}", 3, 3)
                create_mux(f"SB_BIG.P{plane}.D4_{i+1}", f"SB_BIG.P{plane}.Y{i+1}", 3, 4)
                create_mux(f"SB_BIG.P{plane}.D5_{i+1}", f"SB_BIG.P{plane}.Y{i+1}", 3, 5)
                create_mux(f"SB_BIG.P{plane}.D6_{i+1}", f"SB_BIG.P{plane}.Y{i+1}", 3, 6)
                create_mux(f"SB_BIG.P{plane}.D7_{i+1}", f"SB_BIG.P{plane}.Y{i+1}", 3, 7)

            # YDIAG output mux
            create_mux(f"SB_BIG.P{plane}.Y1",  f"SB_BIG.P{plane}.YDIAG", 3, 0)
            create_mux(f"SB_BIG.P{plane}.Y2",  f"SB_BIG.P{plane}.YDIAG", 3, 1)
            create_mux(f"SB_BIG.P{plane}.Y3",  f"SB_BIG.P{plane}.YDIAG", 3, 2)
            create_mux(f"SB_BIG.P{plane}.Y4",  f"SB_BIG.P{plane}.YDIAG", 3, 3)
            create_mux(f"SB_BIG.P{plane}.X34", f"SB_BIG.P{plane}.YDIAG", 3, 4)
            create_mux(f"SB_BIG.P{plane}.X14", f"SB_BIG.P{plane}.YDIAG", 3, 5)
            create_mux(f"SB_BIG.P{plane}.X12", f"SB_BIG.P{plane}.YDIAG", 3, 6)
            create_mux(f"SB_BIG.P{plane}.X23", f"SB_BIG.P{plane}.YDIAG", 3, 7)
    if "SML" in type:
        # SB_SML
        for p in range(12):
            plane = f"{p+1:02d}"
            # Per Y output mux
            for i in range(4):
                create_mux(f"SB_SML.P{plane}.D0",       f"SB_SML.P{plane}.Y{i+1}", 2, 0)
                create_mux(f"SB_SML.P{plane}.YDIAG",    f"SB_SML.P{plane}.Y{i+1}", 2, 1)
                create_mux(f"SB_SML.P{plane}.D2_{i+1}", f"SB_SML.P{plane}.Y{i+1}", 2, 2)
                create_mux(f"SB_SML.P{plane}.D3_{i+1}", f"SB_SML.P{plane}.Y{i+1}", 2, 3)

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
    if is_cpe(x,y): # core section
        if is_sb_big(x,y): 
            return "CPE_BIG" # CPE + SB_BIG + INMUX + OUTMUX
        elif is_sb_sml(x,y):
            return "CPE_SML" # CPE + SB_SML + INMUX + OUTMUX
        else:
            return "CPE" # CPE + INMUX
    elif is_sb_big(x,y):
        return "SB_BIG" # SB_BIG
    elif is_sb_sml(x,y):
        return "SB_SML" # SB_SML
    elif is_edge_top(x,y):
        if is_gpio(x,y):
            return "GPIO_T" # GPIO + EDGE_IO + EDGE_T
        elif is_edge_io(x,y):
            return "EDGE_IO_T" # EDGE_IO + EDGE_T
        else:
            return "EDGE_T" # EDGE_T
    elif is_edge_bottom(x,y):
        if is_gpio(x,y):
            return "GPIO_B" # GPIO + EDGE_IO + EDGE_B
        elif is_edge_io(x,y):
            return "EDGE_IO_B" # EDGE_IO + EDGE_B
        else:
            return "EDGE_B" # EDGE_B
    elif is_edge_left(x,y):
        if is_gpio(x,y):
            return "GPIO_L" # GPIO + EDGE_IO + EDGE_L
        elif is_edge_io(x,y):
            return "EDGE_IO_L" # EDGE_IO + EDGE_L
        else:
            return "EDGE_L" # EDGE_L
    elif is_edge_right(x,y):
        if is_gpio(x,y):
            return "GPIO_R" # GPIO + EDGE_IO + EDGE_R
        elif is_edge_io(x,y):
            return "EDGE_IO_R" # EDGE_IO + EDGE_R
        else:
            return "EDGE_R" # EDGE_R
    else:
        return "NONE"

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
