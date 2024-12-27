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

import die
from dataclasses import dataclass
from typing import List

@dataclass
class Die:
    name : str
    die_x : int
    die_y : int

@dataclass
class Chip:
    name : str
    die_width : int
    die_height : int
    dies : List[Die]

    def max_row(self):
        return self.die_height * die.num_rows() - 3

    def max_col(self):
        return self.die_width * die.num_cols() - 3

    def get_tile_types(self,x,y):
        x_pos = (x + 2) % die.num_cols() - 2
        y_pos = (y + 2) % die.num_rows() - 2
        return die.get_tile_types(x_pos,y_pos)

CCGM1_DEVICES = {
    "CCGM1A1":  Chip("CCGM1A1", 1, 1, [
                    Die("1A", 0, 0)
                ]),
    "CCGM1A2":  Chip("CCGM1A2", 1, 2, [
                    Die("1A", 0, 0),
                    Die("1B", 0, 1)
                ]),
    "CCGM1A4":  Chip("CCGM1A4", 2, 2, [
                    Die("1A", 0, 0),
                    Die("1B", 0, 1),
                    Die("2A", 1, 0),
                    Die("2B", 1, 1)
                ])
}

def get_all_devices():
    return CCGM1_DEVICES

def get_device(name):
    return CCGM1_DEVICES[name]
