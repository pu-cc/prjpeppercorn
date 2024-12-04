/*
 *  prjpeppercorn -- GateMate FPGAs Bitstream Documentation and Tools
 *
 *  Copyright (C) 2024  The Project Peppercorn Authors.
 *
 *  Permission to use, copy, modify, and/or distribute this software for any
 *  purpose with or without fee is hereby granted, provided that the above
 *  copyright notice and this permission notice appear in all copies.
 *
 *  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 *  WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 *  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 *  ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 *  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 *  ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 *  OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 *
 */

#include "Chip.hpp"
#include "Util.hpp"

namespace GateMate {

Chip::Chip(std::string name) : Chip::Chip(1) {}

Chip::Chip(int num) : die_num(num)
{
    Die die;
    dies.push_back(die);
}

int Chip::get_max_die() const { return die_num; }

std::string Chip::get_name() const { return stringf("CCGM1A%d", die_num); }

} // namespace GateMate
