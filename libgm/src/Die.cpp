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

Die::Die()
{
    for (int y = 0; y < MAX_ROWS; y++) {
        for (int x = 0; x < MAX_COLS; x++) {
            latch[std::make_pair(x, y)] = std::vector<u_int8_t>();
            latch[std::make_pair(x, y)].reserve(LATCH_BLOCK_SIZE);
        }
    }
    for (int y = 0; y < MAX_RAM_ROWS; y++) {
        for (int x = 0; x < MAX_RAM_COLS; x++) {
            ram[std::make_pair(x, y)] = std::vector<u_int8_t>();
            ram[std::make_pair(x, y)].reserve(LATCH_BLOCK_SIZE);
            ram_data[std::make_pair(x, y)] = std::vector<u_int8_t>();
        }
    }
}

bool Die::is_latch_empty(int x, int y) const { return latch.at(std::make_pair(x, y)).empty(); }

bool Die::is_ram_empty(int x, int y) const { return ram.at(std::make_pair(x, y)).empty(); }

bool Die::is_ram_data_empty(int x, int y) const { return ram_data.at(std::make_pair(x, y)).empty(); }

void Die::write_latch(int x, int y, const std::vector<uint8_t> &data)
{
    int pos = 0;
    auto &block = latch.at(std::make_pair(x, y));
    block.resize(LATCH_BLOCK_SIZE, 0x00);
    for (auto d : data)
        block[pos++] = d;
}

void Die::write_ram(int x, int y, const std::vector<uint8_t> &data)
{
    int pos = 0;
    auto &block = ram.at(std::make_pair(x, y));
    block.resize(RAM_BLOCK_SIZE, 0x00);
    for (auto d : data)
        block[pos++] = d;
}

void Die::write_ram_data(int x, int y, const std::vector<uint8_t> &data, uint16_t addr)
{
    int pos = addr;
    auto &block = ram_data.at(std::make_pair(x, y));
    block.resize(MEMORY_SIZE, 0x00);
    for (auto d : data)
        block[pos++] = d;
}

} // namespace GateMate
