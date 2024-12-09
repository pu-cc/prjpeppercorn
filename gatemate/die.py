def max_row():
    return 131

def max_col():
    return 163

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

