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

#include "Die.hpp"
#include "Util.hpp"

namespace GateMate {

Die::Die() { clear(); }

void Die::clear()
{
    memset(latch, 0, sizeof(uint8_t) * MAX_ROWS * MAX_COLS * LATCH_BLOCK_SIZE);
    memset(ram, 0, sizeof(uint8_t) * MAX_RAM * RAM_BLOCK_SIZE);
    memset(ram_data, 0, sizeof(uint8_t) * MAX_RAM * MEMORY_SIZE);
}

bool Die::is_latch_empty(int x, int y) const
{
    for (int i = 0; i < LATCH_BLOCK_SIZE; i++)
        if (latch[y * MAX_COLS + x][i] != 0)
            return false;
    return true;
}

bool Die::is_ram_empty(int x, int y) const
{
    for (int i = 0; i < RAM_BLOCK_SIZE; i++)
        if (ram[y * MAX_RAM_COLS + x][i] != 0)
            return false;
    return true;
}

bool Die::is_ram_data_empty(int x, int y) const
{
    for (int i = 0; i < MEMORY_SIZE; i++)
        if (ram_data[y * MAX_RAM_COLS + x][i] != 0)
            return false;
    return true;
}

void Die::write_latch(int x, int y, const std::vector<uint8_t> &data)
{
    int pos = 0;
    for (auto d : data)
        latch[y * MAX_COLS + x][pos++] = d;
}

void Die::write_ram(int x, int y, const std::vector<uint8_t> &data)
{
    int pos = 0;
    for (auto d : data)
        ram[y * MAX_RAM_COLS + x][pos++] = d;
}

void Die::write_ram_data(int x, int y, const std::vector<uint8_t> &data, uint16_t addr)
{
    int pos = addr;
    for (auto d : data)
        ram_data[y * MAX_RAM_COLS + x][pos++] = d;
}

} // namespace GateMate
