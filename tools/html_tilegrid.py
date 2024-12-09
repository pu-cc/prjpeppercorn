#!/usr/bin/env python3
import sys
import argparse
import die

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('family', type=str,
					help="FPGA family (e.g. CCGM1)")
parser.add_argument('device', type=str,
					help="FPGA device (e.g. A1)")
parser.add_argument('outfile', type=argparse.FileType('w'),
                    help="output HTML file")


def get_colour(ttype):
    colour = "#FFFFFF"
    if ttype.startswith("SB_BIG"):
        colour = "#73fc03"
    elif ttype.startswith("SB_SML"):
        colour = "#F0FC03"
    elif ttype.startswith("GPIO"):
        colour = "#88FFFF"
    elif ttype.startswith("INMUX"):
        colour = "#FF9040"
    elif ttype.startswith("OUTMUX"):
        colour = "#9040FF"
    elif ttype.startswith("EDGE_IO"):
        colour = "#6d6d6d"
    elif ttype.startswith("EDGE_"):
        colour = "#DDDDDD"
    else:
        colour = "#888888"
    return colour

def main(argv):
    args = parser.parse_args(argv[1:])

    max_row = die.max_row()
    max_col = die.max_col()
    tiles = []

    for i in range(-2, max_row+1):
        row = []
        for j in range(-2, max_col+1):
            row.append([])
        tiles.append(row)

    for y in range(-2, max_row+1):
        for x in range(-2, max_col+1):
            if die.is_sb_big(x,y):
                tiles[max_row-y][x+2].append((f"{x},{y}", "SB_BIG"))
            if die.is_sb_sml(x,y):
                tiles[max_row-y][x+2].append((f"{x},{y}", "SB_SML"))
            if die.is_cpe(x,y):
                tiles[max_row-y][x+2].append((f"{x},{y}", "CPE"))
                tiles[max_row-y][x+2].append((f"{x},{y}", "INMUX"))
                if die.is_outmux(x,y):
                    tiles[max_row-y][x+2].append((f"{x},{y}", "OUTMUX"))
            if die.is_edge_left(x,y):
                tiles[max_row-y][x+2].append((f"{x},{y}", "EDGE_L"))
            if die.is_edge_right(x,y):
                tiles[max_row-y][x+2].append((f"{x},{y}", "EDGE_R"))
            if die.is_edge_bottom(x,y):
                tiles[max_row-y][x+2].append((f"{x},{y}", "EDGE_B"))
            if die.is_edge_top(x,y):
                tiles[max_row-y][x+2].append((f"{x},{y}", "EDGE_T"))

            if die.is_gpio(x,y):
                tiles[max_row-y][x+2].append((f"{x},{y}", "GPIO"))
            if die.is_edge_io(x,y):
                tiles[max_row-y][x+2].append((f"{x},{y}", "EDGE_IO"))

    f = args.outfile
    print(
        f"""<html>
            <head><title>{args.family} Tiles</title></head>
            <body>
            <h1>{args.device} Tilegrid</h1>
            <table style='font-size: 8pt; border: 2px solid black; text-align: center'>
        """, file=f)
    for trow in tiles:
        print("<tr>", file=f)
        row_max_height = 0
        for tloc in trow:
            row_max_height = max(row_max_height, len(tloc))
        row_height = max(75, 30 * row_max_height)
        for tloc in trow:
            print(f"<td style='border: 2px solid black; height: {row_height}px'>", file=f)
            for tile in tloc:
                print(f"<div style='height: {100 / len(tloc)}%; background-color: {get_colour(tile[1])}'><em>{tile[0]}</em><br/><strong>{tile[1]}</strong></div>", file=f)
            print("</td>", file=f)
        print("</tr>", file=f)
    print("</table></body></html>", file=f)


if __name__ == "__main__":
    main(sys.argv)
