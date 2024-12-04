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

#ifndef LIBGATEMATE_DIE_HPP
#define LIBGATEMATE_DIE_HPP

#include <cstdint>
#include <string>
#include <vector>

namespace GateMate {

class Die
{
  public:
    static constexpr int MAX_ROWS = 66;
    static constexpr int MAX_COLS = 82;
    static constexpr int MAX_RAM = 32;
    static constexpr int MAX_RAM_ROWS = 8;
    static constexpr int MAX_RAM_COLS = 4;
    static constexpr int LATCH_BLOCK_SIZE = 112;
    static constexpr int RAM_BLOCK_SIZE = 27;
    static constexpr int MEMORY_SIZE = 5120;

  public:
    explicit Die();

    // Get max row and column
    int get_max_row() const { return MAX_ROWS; }
    int get_max_col() const { return MAX_COLS; }
    int get_max_ram_row() const { return MAX_RAM_ROWS; }
    int get_max_ram_col() const { return MAX_RAM_COLS; }

    void clear();

    bool is_latch_empty(int x, int y) const;
    bool is_ram_empty(int x, int y) const;
    bool is_ram_data_empty(int x, int y) const;

    void write_latch(int x, int y, const std::vector<uint8_t> &data);
    void write_ram(int x, int y, const std::vector<uint8_t> &data);
    void write_ram_data(int x, int y, const std::vector<uint8_t> &data, uint16_t addr);

    const uint8_t *get_latch_config(int x, int y) const { return &latch[y * MAX_COLS + x][0]; }
    const uint8_t *get_ram_config(int x, int y) const { return &ram[y * MAX_RAM_COLS + x][0]; }
    const uint8_t *get_ram_data(int x, int y) const { return &ram_data[y * MAX_RAM_COLS + x][0]; }

  private:
    uint8_t latch[MAX_ROWS * MAX_COLS][LATCH_BLOCK_SIZE]; // Config latches
    uint8_t ram[MAX_RAM][RAM_BLOCK_SIZE];                 // Config RAM
    uint8_t ram_data[MAX_RAM][MEMORY_SIZE];               // RAM data content FRAM
};

} // namespace GateMate

#endif // LIBGATEMATE_DIE_HPP
