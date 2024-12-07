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

#include "TileBitDatabase.hpp"
#include <iomanip>
#include <iostream>
#include <sstream>
#include "Chip.hpp"
#include "ChipConfig.hpp"
#include "Util.hpp"

namespace GateMate {

std::vector<bool> data_bytes_to_array(const vector<uint8_t> &data, size_t count)
{
    std::vector<bool> result(count * 8);
    for (size_t j = 0; j < count; j++) {
        uint8_t val = data[j];
        for (size_t i = 0; i < 8; i++) {
            uint8_t temp = 1 << i;
            if (val & temp)
                result[j * 8 + i] = true;
            else
                result[j * 8 + i] = false;
        }
    }
    return result;
}

bool is_array_empty(std::vector<bool> &array)
{
    for (bool val : array)
        if (val)
            return false;
    return true;
}

BaseBitDatabase::BaseBitDatabase(int num_bits) : num_bits(num_bits), known_bits(num_bits, false) {}
BaseBitDatabase::~BaseBitDatabase() {}

void BaseBitDatabase::add_word_settings(const std::string &name, int start, int end)
{
    if (words.find(name) != words.end())
        throw DatabaseConflictError(fmt("word " << name << " already exists in DB"));

    for (int i = start; i < start + end; i++) {
        if (known_bits[i])
            throw DatabaseConflictError(fmt("bit " << i << " for word " << name << " already mapped"));
        known_bits[i] = true;
    }
    words[name] = {start, start + end};
}

void BaseBitDatabase::add_unknowns()
{
    for (int i = 0; i < num_bits; i++) {
        if (!known_bits[i])
            words[stringf("UNKNOWN_%03d", i)] = {i, i + 1};
    }
}

std::vector<uint8_t> BaseBitDatabase::bits_to_bytes(std::vector<bool> &bits)
{
    std::vector<uint8_t> val;
    size_t pos = 0;
    for (size_t j = 0; j < bits.size() / 8; j++) {
        uint8_t data = 0;
        for (int i = 0; i < 8; i++) {
            data >>= 1;
            data |= bits[pos] ? 0x80 : 0x00;
            pos++;
        }
        val.push_back(data);
    }
    return val;
}

std::vector<uint8_t> BaseBitDatabase::config_to_data(const TileConfig &cfg)
{
    std::vector<bool> tile(num_bits, false);
    for (auto &w : cfg.cwords) {
        words[w.name].set_value(tile, w.value);
    }
    return bits_to_bytes(tile);
}

TileConfig BaseBitDatabase::data_to_config(const vector<uint8_t> &data)
{
    TileConfig cfg;
    std::vector<bool> d = data_bytes_to_array(data, num_bits * 8);
    for (auto &w : words) {
        auto val = w.second.get_value(d);
        if (is_array_empty(val))
            continue;
        cfg.add_word(w.first, val);
    }
    return cfg;
}

void TileBitDatabase::add_sb_big(int index, int start) { add_word_settings(stringf("SB_BIG_%02d", index), start, 15); }

void TileBitDatabase::add_sb_sml(int index, int start) { add_word_settings(stringf("SB_SML_%02d", index), start, 12); }

void TileBitDatabase::add_sb_drive(int index, int start)
{
    add_word_settings(stringf("SB_DRIVE_%02d", index), start, 4);
}

void TileBitDatabase::add_cpe(int index, int start) { add_word_settings(stringf("CPE_%d", index), start, 80); }

void TileBitDatabase::add_ff_init(int index, int start)
{
    add_word_settings(stringf("CPE_%d.FF_INIT", index), start, 2);
}

void TileBitDatabase::add_inmux(int index, int plane, int start)
{
    add_word_settings(stringf("INMUX_%d_%02d", index, plane), start, 4);
}

void TileBitDatabase::add_gpio(int start) { add_word_settings("GPIO", start, 72); }

void TileBitDatabase::add_edge_io(int index, int start) { add_word_settings(stringf("EDGE_IO_%d", index), start, 16); }

void TileBitDatabase::add_right_edge(int index, int start)
{
    add_word_settings(stringf("RIGHT_EDGE_%d", index), start, 24);
}

void TileBitDatabase::add_left_edge(int index, int start)
{
    add_word_settings(stringf("LEFT_EDGE_%d", index), start, 24);
}

void TileBitDatabase::add_top_edge(int index, int start)
{
    add_word_settings(stringf("TOP_EDGE_%d", index), start, 24);
}

void TileBitDatabase::add_bottom_edge(int index, int start)
{
    add_word_settings(stringf("BOTTOM_EDGE_%d", index), start, 48);
}

TileBitDatabase::TileBitDatabase(const int x, const int y) : BaseBitDatabase(Die::LATCH_BLOCK_SIZE * 8)
{
    bool is_core = false;
    if (y == 0) {
        add_bottom_edge(1, 13 * 8);
        add_bottom_edge(2, 19 * 8);
    } else if (x == 0) {
        add_left_edge(1, 13 * 8);
        add_left_edge(2, 16 * 8);
    } else if (y == 66 - 1) {
        add_top_edge(1, 13 * 8);
        add_top_edge(2, 16 * 8);
    } else if (x == 82 - 1) {
        add_right_edge(1, 13 * 8);
        add_right_edge(2, 16 * 8);
    } else {
        is_core = true;
        for (int i = 0; i < 4; i++) {
            add_cpe(i + 1, 10 * i * 8);
            add_ff_init(i + 1, (Die::LATCH_BLOCK_SIZE - 1) * 8 + i * 2);
        }
        int pos = 40;
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 6; j++) {
                add_inmux(i + 1, j * 2 + 1, pos * 8);
                add_inmux(i + 1, j * 2 + 2, pos * 8 + 4);
                pos++;
            }
        }
    }
    if (!is_core) {
        add_gpio(0);
        add_edge_io(1, 9 * 8);
        add_edge_io(2, 11 * 8);
    }

    int pos = 64;

    // All tiles have switch boxes

    // 64 SB_BIG plane 1
    // 65 SB_BIG plane 1
    // 66 SB_DRIVE plane 2,1
    // 67 SB_BIG plane 2
    // 68 SB_BIG plane 2
    // repeated to cover all 12 planes
    for (int i = 0; i < 6; i++) {
        add_sb_big(i * 2 + 1, pos * 8);
        add_sb_drive(i * 2 + 1, (pos + 2) * 8);
        add_sb_drive(i * 2 + 2, (pos + 2) * 8 + 4);
        add_sb_big(i * 2 + 2, (pos + 3) * 8);
        pos += 5;
    }
    // 94 SB_SML plane 1
    // 95 SB_SML plane 2,1
    // 96 SB_SML plane 2
    // repeated to cover all 12 planes
    for (int i = 0; i < 6; i++) {
        add_sb_sml(i * 2 + 1, pos * 8);
        add_sb_sml(i * 2 + 2, (pos + 1) * 8 + 4);
        pos += 3;
    }
    add_unknowns();
}

RamBitDatabase::RamBitDatabase() : BaseBitDatabase(Die::RAM_BLOCK_SIZE * 8)
{
    add_word_settings("RAM_cfg_forward_a_addr", 0 * 8, 8);
    add_word_settings("RAM_cfg_forward_b_addr", 1 * 8, 8);
    add_word_settings("RAM_cfg_forward_a0_clk", 2 * 8, 8);
    add_word_settings("RAM_cfg_forward_a0_en", 3 * 8, 8);
    add_word_settings("RAM_cfg_forward_a0_we", 4 * 8, 8);
    add_word_settings("RAM_cfg_forward_a1_clk", 5 * 8, 8);
    add_word_settings("RAM_cfg_forward_a1_en", 6 * 8, 8);
    add_word_settings("RAM_cfg_forward_a1_we", 7 * 8, 8);
    add_word_settings("RAM_cfg_forward_b0_clk", 8 * 8, 8);
    add_word_settings("RAM_cfg_forward_b0_en", 9 * 8, 8);
    add_word_settings("RAM_cfg_forward_b0_we", 10 * 8, 8);
    add_word_settings("RAM_cfg_forward_b1_clk", 11 * 8, 8);
    add_word_settings("RAM_cfg_forward_b1_en", 12 * 8, 8);
    add_word_settings("RAM_cfg_forward_b1_we", 13 * 8, 8);
    add_word_settings("RAM_cfg_sram_mode_i_cfg", 14 * 8, 8);
    add_word_settings("RAM_cfg_in_out_cfg", 15 * 8, 8);
    add_word_settings("RAM_cfg_out_cfg", 16 * 8, 8);
    add_word_settings("RAM_cfg_out_b1_cfg", 17 * 8, 8);
    add_word_settings("RAM_cfg_wrmode_outreg", 18 * 8, 8);
    add_word_settings("RAM_cfg_inversion", 19 * 8, 8);
    add_word_settings("RAM_cfg_inv_ecc_dyn", 20 * 8, 8);
    add_word_settings("RAM_cfg_fifo_sync_empty", 21 * 8, 8);
    add_word_settings("RAM_cfg_fifo_empty", 22 * 8, 8);
    add_word_settings("RAM_cfg_fifo_aync_full", 23 * 8, 8);
    add_word_settings("RAM_cfg_fifo_full", 24 * 8, 8);
    add_word_settings("RAM_cfg_sram_delay", 25 * 8, 8);
    add_word_settings("RAM_cfg_datbm_cascade", 26 * 8, 8);
    add_unknowns();
}

ConfigBitDatabase::ConfigBitDatabase() : BaseBitDatabase(Die::DIE_CONFIG_SIZE * 8)
{
    int pos = 0;
    for (int i = 0; i < 4; i++) {
        add_word_settings(stringf("PLL%d.CFG_A", i), pos, 96);
        pos += 96;
        add_word_settings(stringf("PLL%d.CFG_B", i), pos, 96);
        pos += 96;
    }
    add_word_settings("CLKIN.PLL0", pos + 0, 8);
    add_word_settings("CLKIN.PLL1", pos + 8, 8);
    add_word_settings("CLKIN.PLL2", pos + 16, 8);
    add_word_settings("CLKIN.PLL3", pos + 24, 8);
    add_word_settings("GLBOUT.PLL0", pos + 32, 16);
    add_word_settings("GLBOUT.PLL1", pos + 48, 16);
    add_word_settings("GLBOUT.PLL2", pos + 64, 16);
    add_word_settings("GLBOUT.PLL3", pos + 80, 16);

    pos = Die::STATUS_CFG_START * 8;
    add_word_settings("GPIO.BANK_S1", pos + 16, 1);
    add_word_settings("GPIO.BANK_S2", pos + 17, 1);
    add_word_settings("GPIO.BANK_CFG", pos + 19, 1);
    add_word_settings("GPIO.BANK_E1", pos + 20, 1);
    add_word_settings("GPIO.BANK_E2", pos + 21, 1);

    add_word_settings("GPIO.BANK_N1", pos + 24, 1);
    add_word_settings("GPIO.BANK_N2", pos + 25, 1);

    add_word_settings("GPIO.BANK_W1", pos + 28, 1);
    add_word_settings("GPIO.BANK_W2", pos + 29, 1);

    pos += 32;
    for (int i = 0; i < Die::MAX_PLL; i++) {
        add_word_settings(stringf("PLL%d.CTRL_A", i), pos + 0, 8);
        add_word_settings(stringf("PLL%d.CTRL_B", i), pos + 8, 8);
        pos += 16;
    }
}

vector<bool> WordSettingBits::get_value(const vector<bool> &tile) const
{
    std::vector<bool> val;
    for (int i = start; i < end; i++)
        val.push_back(tile[i]);
    return val;
}

void WordSettingBits::set_value(vector<bool> &tile, const vector<bool> &value) const
{
    for (int i = start; i < end; i++)
        tile[i] = value[i - start];
}

DatabaseConflictError::DatabaseConflictError(const string &desc) : runtime_error(desc) {}

} // namespace GateMate