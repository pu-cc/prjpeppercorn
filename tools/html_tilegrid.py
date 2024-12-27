#!/usr/bin/env python3
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

import sys
import argparse
import chip
import die

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('family', type=str,
					help="FPGA family (e.g. CCGM1)")
parser.add_argument('device', type=str,
					help="FPGA device (e.g. A1)")
parser.add_argument('outfile', type=argparse.FileType('w'),
                    help="output HTML file")


def get_colour(ttype):
    match ttype:
        case "CPE":
            colour = "#ACC8E6"
        case "SB_BIG":
            colour = "#9CC763"
        case "SB_SML":
            colour = "#F8EA56"
        case "GPIO":
            colour = "#B699D4"
        case "IM":
            colour = "#FFC51F"
        case "OM":
            colour = "#D19537"
        case "IOES":
            colour = "#6D6D6D"
        case "LES" | "RES" | "TES" | "BES":
            colour = "#FDD3D3"
        case "PLL":
            colour = "#FF7ABE"
        case "SERDES":
            colour = "#64FF65"
        case _:
            colour = "#FFFFFF"
    return colour

def main(argv):
    args = parser.parse_args(argv[1:])
    ch = chip.get_device(args.device)

    max_row = ch.max_row()
    max_col = ch.max_col()
    tiles = []

    for i in range(-2, max_row+1):
        row = []
        for j in range(-2, max_col+1):
            row.append([])
        tiles.append(row)

    for y in range(-2, max_row+1):
        for x in range(-2, max_col+1):
            for type in ch.get_tile_types(x,y):
                tiles[max_row-y][x+2].append((f"{x},{y}", type))

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
        row_height = max(90, 30 * row_max_height)
        for tloc in trow:
            print(f"<td style='border: 2px solid black; height: {row_height}px'>", file=f)
            for tile in tloc:
                print(f"<div style='height: {100 / len(tloc)}%; background-color: {get_colour(tile[1])}'><em>{tile[0]}</em><br/><strong>{tile[1]}</strong></div>", file=f)
            print("</td>", file=f)
        print("</tr>", file=f)
    print("</table></body></html>", file=f)


if __name__ == "__main__":
    main(sys.argv)
