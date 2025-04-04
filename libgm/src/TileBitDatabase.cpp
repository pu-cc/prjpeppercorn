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

std::vector<bool> data_bytes_to_array(const std::vector<uint8_t> &data, size_t count)
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

void BaseBitDatabase::add_word_settings(const std::string &name, int start, int len)
{
    if (words.find(name) != words.end())
        throw DatabaseConflictError(fmt("word " << name << " already exists in DB"));

    for (int i = start; i < start + len; i++) {
        if (known_bits[i])
            throw DatabaseConflictError(fmt("bit " << i << " for word " << name << " already mapped"));
        known_bits[i] = true;
    }
    words[name] = {start, start + len};
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
        if (words.count(w.name)) {
            words[w.name].set_value(tile, w.value);
        } else {
            throw std::runtime_error(fmt("unknown word " << w.name << " found while converting data"));
        }
    }
    return bits_to_bytes(tile);
}

TileConfig BaseBitDatabase::data_to_config(const std::vector<uint8_t> &data)
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

void TileBitDatabase::add_sb_big(int index, int start)
{
    add_word_settings(stringf("SB_BIG.P%02d.YDIAG", index), start + 0, 3);
    add_word_settings(stringf("SB_BIG.P%02d.Y1", index), start + 3, 3);
    add_word_settings(stringf("SB_BIG.P%02d.Y2", index), start + 6, 3);
    add_word_settings(stringf("SB_BIG.P%02d.Y3", index), start + 9, 3);
    add_word_settings(stringf("SB_BIG.P%02d.Y4", index), start + 12, 3);
}

void TileBitDatabase::add_sb_sml(int index, int start)
{
    add_word_settings(stringf("SB_SML.P%02d.YDIAG", index), start + 0, 3);
    add_word_settings(stringf("SB_SML.P%02d.Y1", index), start + 3, 2);
    add_word_settings(stringf("SB_SML.P%02d.Y2", index), start + 5, 2);
    add_word_settings(stringf("SB_SML.P%02d.Y3", index), start + 7, 2);
    add_word_settings(stringf("SB_SML.P%02d.Y4", index), start + 9, 2);
}

void TileBitDatabase::add_sb_drive(int index, int start)
{
    for (int i = 0; i < 4; i++)
        add_word_settings(stringf("SB_DRIVE.P%02d.D%d", index, i + 1), start + i, 1);
}

void TileBitDatabase::add_cpe(int index, int start)
{
    add_word_settings(stringf("CPE%d.INIT_L00", index), start + 0, 4);
    add_word_settings(stringf("CPE%d.INIT_L01", index), start + 4, 4);
    add_word_settings(stringf("CPE%d.INIT_L02", index), start + 8, 4);
    add_word_settings(stringf("CPE%d.INIT_L03", index), start + 12, 4);

    add_word_settings(stringf("CPE%d.INIT_L10", index), start + 16, 4);
    add_word_settings(stringf("CPE%d.INIT_L11", index), start + 20, 4);

    add_word_settings(stringf("CPE%d.INIT_L20", index), start + 24, 4);

    add_word_settings(stringf("CPE%d.INIT_L30", index), start + 28, 4);

    add_word_settings(stringf("CPE%d.C_I1", index), start + 32, 1);
    add_word_settings(stringf("CPE%d.C_I2", index), start + 33, 1);
    add_word_settings(stringf("CPE%d.C_I3", index), start + 34, 1);
    add_word_settings(stringf("CPE%d.C_I4", index), start + 35, 1);

    add_word_settings(stringf("CPE%d.C_FUNCTION", index), start + 36, 3);
    add_word_settings(stringf("CPE%d.C_COMP", index), start + 39, 1);
    add_word_settings(stringf("CPE%d.C_COMP_I", index), start + 40, 1);
    add_word_settings(stringf("CPE%d.C_HORIZ", index), start + 41, 1);
    add_word_settings(stringf("CPE%d.C_SELX", index), start + 42, 1);
    add_word_settings(stringf("CPE%d.C_SELY1", index), start + 43, 1);
    add_word_settings(stringf("CPE%d.C_SELY2", index), start + 44, 1);
    add_word_settings(stringf("CPE%d.C_SEL_C", index), start + 45, 1);
    add_word_settings(stringf("CPE%d.C_SEL_P", index), start + 46, 1);
    add_word_settings(stringf("CPE%d.C_Y12", index), start + 47, 1);
    add_word_settings(stringf("CPE%d.C_CX_I", index), start + 48, 1);
    add_word_settings(stringf("CPE%d.C_CY1_I", index), start + 49, 1);
    add_word_settings(stringf("CPE%d.C_CY2_I", index), start + 50, 1);
    add_word_settings(stringf("CPE%d.C_PX_I", index), start + 51, 1);
    add_word_settings(stringf("CPE%d.C_PY1_I", index), start + 52, 1);
    add_word_settings(stringf("CPE%d.C_PY2_I", index), start + 53, 1);
    add_word_settings(stringf("CPE%d.C_C_P", index), start + 54, 1);
    add_word_settings(stringf("CPE%d.C_2D_IN", index), start + 55, 1);
    add_word_settings(stringf("CPE%d.C_SN", index), start + 56, 3);
    add_word_settings(stringf("CPE%d.C_O1", index), start + 59, 2);
    add_word_settings(stringf("CPE%d.C_O2", index), start + 61, 2);
    add_word_settings(stringf("CPE%d.C_BR", index), start + 63, 1);

    add_word_settings(stringf("CPE%d.C_CPE_CLK", index), start + 64, 2);
    add_word_settings(stringf("CPE%d.C_CPE_EN", index), start + 66, 2);
    add_word_settings(stringf("CPE%d.C_CPE_RES", index), start + 68, 2);
    add_word_settings(stringf("CPE%d.C_CPE_SET", index), start + 70, 2);

    add_word_settings(stringf("CPE%d.C_RAM_I1", index), start + 72, 1);
    add_word_settings(stringf("CPE%d.C_RAM_I2", index), start + 73, 1);
    add_word_settings(stringf("CPE%d.C_RAM_O1", index), start + 74, 1);
    add_word_settings(stringf("CPE%d.C_RAM_O2", index), start + 75, 1);
    add_word_settings(stringf("CPE%d.C_L_D", index), start + 76, 1);
    add_word_settings(stringf("CPE%d.C_EN_SR", index), start + 77, 1);
    add_word_settings(stringf("CPE%d.C_CLKSEL", index), start + 78, 1);
    add_word_settings(stringf("CPE%d.C_ENSEL", index), start + 79, 1);
}

void TileBitDatabase::add_ff_init(int index, int start)
{
    add_word_settings(stringf("CPE%d.FF_INIT", index), start, 2);
}

void TileBitDatabase::add_inmux(int index, int plane, int start)
{
    add_word_settings(stringf("IM%d.P%02d", index, plane), start, 3);
}

void TileBitDatabase::add_outmux(int index, int plane, int start)
{
    add_word_settings(stringf("OM%d.P%02d", index, plane), start, 2);
}

void TileBitDatabase::add_gpio(int start)
{
    add_word_settings("GPIO.OPEN_DRAIN", start + 0, 1);
    add_word_settings("GPIO.SLEW", start + 1, 1);
    add_word_settings("GPIO.DRIVE", start + 2, 2);
    add_word_settings("GPIO.INPUT_ENABLE", start + 4, 1);
    add_word_settings("GPIO.PULLDOWN", start + 5, 1);
    add_word_settings("GPIO.PULLUP", start + 6, 1);
    add_word_settings("GPIO.SCHMITT_TRIGGER", start + 7, 1);

    add_word_settings("GPIO.OUT_SIGNAL", start + 8, 1);

    add_word_settings("GPIO.OUT1_4", start + 9, 1);
    add_word_settings("GPIO.OUT2_3", start + 10, 1);
    add_word_settings("GPIO.OUT23_14_SEL", start + 11, 1);

    add_word_settings("GPIO.USE_CFG_BIT", start + 12, 1); // Use bit 9 for clock, error in silicon
    add_word_settings("GPIO.USE_DDR", start + 13, 1);

    add_word_settings("GPIO.SEL_IN_CLOCK", start + 14, 1);  // Use clock signals for IN CLK
    add_word_settings("GPIO.SEL_OUT_CLOCK", start + 15, 1); // Use clock signals for OUT CLK

    add_word_settings("GPIO.OE_ENABLE", start + 16, 1);
    add_word_settings("GPIO.OE_SIGNAL", start + 17, 2); // 0 is constant 1
    // 19 unused
    add_word_settings("GPIO.OUT1_FF", start + 20, 1);
    add_word_settings("GPIO.OUT2_FF", start + 21, 1);
    add_word_settings("GPIO.IN1_FF", start + 22, 1);
    add_word_settings("GPIO.IN2_FF", start + 23, 1);

    add_word_settings("GPIO.OUT_CLOCK", start + 24, 2);
    add_word_settings("GPIO.INV_OUT1_CLOCK", start + 26, 1);
    add_word_settings("GPIO.INV_OUT2_CLOCK", start + 27, 1);
    add_word_settings("GPIO.IN_CLOCK", start + 28, 2);
    add_word_settings("GPIO.INV_IN1_CLOCK", start + 30, 1);
    add_word_settings("GPIO.INV_IN2_CLOCK", start + 31, 1);

    add_word_settings("GPIO.DELAY_OBF", start + 32, 16);
    add_word_settings("GPIO.DELAY_IBF", start + 48, 16);

    add_word_settings("GPIO.LVDS_EN", start + 64, 1);
    add_word_settings("GPIO.LVDS_BOOST", start + 65, 1);
    add_word_settings("GPIO.LVDS_IE", start + 66, 1);
    add_word_settings("GPIO.LVDS_RTERM", start + 67, 1);
}

void TileBitDatabase::add_edge_io(int index, int start)
{
    for (int i = 0; i < 12; i++)
        add_word_settings(stringf("IOES%d.SB_IN_%02d", index, i + 1), start + i, 1);
}

void TileBitDatabase::add_right_edge(int index, int start)
{
    add_word_settings(stringf("RES%d.SEL_MDIE1",  index), start + 0, 1);
    add_word_settings(stringf("RES%d.SEL_MDIE2",  index), start + 1, 1);
    add_word_settings(stringf("RES%d.SEL_MDIE3",  index), start + 2, 1);
    add_word_settings(stringf("RES%d.SEL_MDIE4",  index), start + 3, 1);
    add_word_settings(stringf("RES%d.SEL_MDIE5",  index), start + 4, 1);
    add_word_settings(stringf("RES%d.SEL_MDIE6",  index), start + 5, 1);
    add_word_settings(stringf("RES%d.SEL_MDIE7",  index), start + 6, 1);
    add_word_settings(stringf("RES%d.SEL_MDIE8",  index), start + 7, 1);

    add_word_settings(stringf("RES%d.SIG_SEL1",   index), start + 8 , 3);
    add_word_settings(stringf("RES%d.SIG_SEL2",   index), start + 11, 3);
    add_word_settings(stringf("RES%d.SIG_SEL3",   index), start + 14, 3);
    add_word_settings(stringf("RES%d.SIG_SEL4",   index), start + 17, 3);
}

void TileBitDatabase::add_left_edge(int index, int start)
{
    add_word_settings(stringf("LES%d.SB_Y3_SEL1", index), start + 0 , 3);
    add_word_settings(stringf("LES%d.MDIE1_SEL1", index), start + 3 , 3);
    add_word_settings(stringf("LES%d.CLOCK_SEL1", index), start + 6 , 2);

    add_word_settings(stringf("LES%d.SB_Y3_SEL2", index), start + 8 , 3);
    add_word_settings(stringf("LES%d.MDIE1_SEL2", index), start + 11, 3);
    add_word_settings(stringf("LES%d.CLOCK_SEL2", index), start + 14, 2);

    add_word_settings(stringf("LES%d.CINX_CONST", index), start + 16, 1);
    add_word_settings(stringf("LES%d.CINX_SEL",   index), start + 17, 2);
    
    add_word_settings(stringf("LES%d.PINX_CONST", index), start + 19, 1);
    add_word_settings(stringf("LES%d.PINX_SEL",   index), start + 20, 2);
}

void TileBitDatabase::add_top_edge(int index, int start)
{
    add_word_settings(stringf("TES%d.SEL_MDIE1",  index), start + 0, 1);
    add_word_settings(stringf("TES%d.SEL_MDIE2",  index), start + 1, 1);
    add_word_settings(stringf("TES%d.SEL_MDIE3",  index), start + 2, 1);
    add_word_settings(stringf("TES%d.SEL_MDIE4",  index), start + 3, 1);
    add_word_settings(stringf("TES%d.SEL_MDIE5",  index), start + 4, 1);
    add_word_settings(stringf("TES%d.SEL_MDIE6",  index), start + 5, 1);
    add_word_settings(stringf("TES%d.SEL_MDIE7",  index), start + 6, 1);
    add_word_settings(stringf("TES%d.SEL_MDIE8",  index), start + 7, 1);

    add_word_settings(stringf("TES%d.SIG_SEL1",   index), start + 8 , 3);
    add_word_settings(stringf("TES%d.SIG_SEL2",   index), start + 11, 3);
    add_word_settings(stringf("TES%d.SIG_SEL3",   index), start + 14, 3);
    add_word_settings(stringf("TES%d.SIG_SEL4",   index), start + 17, 3);
}

void TileBitDatabase::add_bottom_edge(int index, int start)
{
    add_word_settings(stringf("BES%d.SB_Y4_SEL1", index), start + 0 , 3);
    add_word_settings(stringf("BES%d.MDIE2_SEL1", index), start + 3 , 3);
    add_word_settings(stringf("BES%d.CLOCK_SEL1", index), start + 6 , 2);

    add_word_settings(stringf("BES%d.SB_Y4_SEL2", index), start + 8 , 3);
    add_word_settings(stringf("BES%d.MDIE2_SEL2", index), start + 11, 3);
    add_word_settings(stringf("BES%d.CLOCK_SEL2", index), start + 14, 2);

    add_word_settings(stringf("BES%d.SB_Y4_SEL3", index), start + 16, 3);
    add_word_settings(stringf("BES%d.MDIE2_SEL3", index), start + 19, 3);
    add_word_settings(stringf("BES%d.CLOCK_SEL3", index), start + 22, 2);

    add_word_settings(stringf("BES%d.SB_Y4_SEL4", index), start + 24, 3);
    add_word_settings(stringf("BES%d.MDIE2_SEL4", index), start + 27, 3);
    add_word_settings(stringf("BES%d.CLOCK_SEL4", index), start + 30, 2);

    add_word_settings(stringf("BES%d.CINY1_CONST",index), start + 32, 1);
    add_word_settings(stringf("BES%d.CINY1_SEL",  index), start + 33, 2);

    add_word_settings(stringf("BES%d.PINY1_CONST",index), start + 35, 1);
    add_word_settings(stringf("BES%d.PINY1_SEL",  index), start + 36, 2);

    add_word_settings(stringf("BES%d.CINY2_CONST",index), start + 38, 1);
    add_word_settings(stringf("BES%d.CINY2_SEL",  index), start + 39, 2);

    add_word_settings(stringf("BES%d.PINY2_CONST",index), start + 41, 1);
    add_word_settings(stringf("BES%d.PINY2_SEL",  index), start + 42, 2);

    add_word_settings(stringf("BES%d.P_CINY1",    index), start + 44, 1);
    add_word_settings(stringf("BES%d.P_PINY1",    index), start + 45, 1);
    add_word_settings(stringf("BES%d.P_CINY2",    index), start + 46, 1);
    add_word_settings(stringf("BES%d.P_PINY2",    index), start + 47, 1);
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
                add_inmux(i + 1, j * 2 + 2, pos * 8 + 3);
                pos++;
            }
        }
        for (int i = 0; i < 2; i++) {
            pos = 54 + i * 6;
            for (int j = 9; j <= 12; j++) {
                add_outmux(i ? 4 : 1, j, pos * 8 + 6);
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

SerdesBitDatabase::SerdesBitDatabase() : BaseBitDatabase(Die::SERDES_CFG_SIZE * 8)
{
    for (int i = 0; i < Die::SERDES_CFG_SIZE/2; i++) {
        add_word_settings(stringf("REG_%02X",i), i*16, 16);
    }
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
    add_word_settings("RAM_cfg_sram_mode", 14 * 8, 2);
    add_word_settings("RAM_cfg_input_config_a0", 14 * 8 + 2, 3);
    add_word_settings("RAM_cfg_input_config_a1", 14 * 8 + 5, 3);
    add_word_settings("RAM_cfg_input_config_b0", 15 * 8 + 1, 3);
    add_word_settings("RAM_cfg_input_config_b1", 15 * 8 + 4, 3);
    add_word_settings("RAM_cfg_output_config_a0", 15 * 8 + 7, 3);
    add_word_settings("RAM_cfg_output_config_a1", 16 * 8 + 2, 3);
    add_word_settings("RAM_cfg_output_config_b0", 16 * 8 + 5, 3);
    add_word_settings("RAM_cfg_output_config_b1", 17 * 8, 3);
    add_word_settings("RAM_cfg_a0_writemode", 18 * 8 + 0, 1);
    add_word_settings("RAM_cfg_a1_writemode", 18 * 8 + 1, 1);
    add_word_settings("RAM_cfg_b0_writemode", 18 * 8 + 2, 1);
    add_word_settings("RAM_cfg_b1_writemode", 18 * 8 + 3, 1);
    add_word_settings("RAM_cfg_a0_set_outputreg", 18 * 8 + 4, 1);
    add_word_settings("RAM_cfg_a1_set_outputreg", 18 * 8 + 5, 1);
    add_word_settings("RAM_cfg_b0_set_outputreg", 18 * 8 + 6, 1);
    add_word_settings("RAM_cfg_b1_set_outputreg", 18 * 8 + 7, 1);
    add_word_settings("RAM_cfg_inversion_a0", 19 * 8, 3);
    add_word_settings("RAM_cfg_inversion_a1", 19 * 8 + 3, 3);
    add_word_settings("RAM_cfg_inversion_b0", 19 * 8 + 6, 3);
    add_word_settings("RAM_cfg_inversion_b1", 20 * 8 + 1, 3);
    add_word_settings("RAM_cfg_ecc_enable", 20 * 8 + 4, 2);
    add_word_settings("RAM_cfg_dyn_stat_select", 20 * 8 + 6, 2);
    add_word_settings("RAM_cfg_almost_empty_offset", 21 * 8, 15);
    add_word_settings("RAM_cfg_fifo_sync_enable", 22 * 8 + 7, 1);
    add_word_settings("RAM_cfg_almost_full_offset", 23 * 8, 15);
    add_word_settings("RAM_cfg_fifo_async_enable", 24 * 8 + 7, 1);
    add_word_settings("RAM_cfg_sram_delay", 25 * 8, 6);
    add_word_settings("RAM_cfg_datbm_sel", 26 * 8, 4);
    add_word_settings("RAM_cfg_cascade_enable", 26 * 8 + 4, 2);
    add_unknowns();
}

void ConfigBitDatabase::add_pll_cfg(int index, char cfg, int start)
{
    add_word_settings(stringf("PLL%d.CFG_%c.CI_FILTER_CONST", index, cfg), start + 0, 5);
    add_word_settings(stringf("PLL%d.CFG_%c.CP_FILTER_CONST", index, cfg), start + 5, 5);
    add_word_settings(stringf("PLL%d.CFG_%c.N1", index, cfg), start + 10, 6);
    add_word_settings(stringf("PLL%d.CFG_%c.N2", index, cfg), start + 16, 10);
    add_word_settings(stringf("PLL%d.CFG_%c.M1", index, cfg), start + 26, 6);
    add_word_settings(stringf("PLL%d.CFG_%c.M2", index, cfg), start + 32, 10);
    add_word_settings(stringf("PLL%d.CFG_%c.K", index, cfg), start + 42, 12);
    add_word_settings(stringf("PLL%d.CFG_%c.FB_PATH", index, cfg), start + 54, 1);
    add_word_settings(stringf("PLL%d.CFG_%c.FINE_TUNE", index, cfg), start + 55, 11);
    add_word_settings(stringf("PLL%d.CFG_%c.COARSE_TUNE", index, cfg), start + 66, 3);
    add_word_settings(stringf("PLL%d.CFG_%c.AO_SW", index, cfg), start + 69, 5);
    add_word_settings(stringf("PLL%d.CFG_%c.OPEN_LOOP", index, cfg), start + 74, 1);
    add_word_settings(stringf("PLL%d.CFG_%c.ENFORCE_LOCK", index, cfg), start + 75, 1);
    add_word_settings(stringf("PLL%d.CFG_%c.PFD_SEL", index, cfg), start + 76, 1);
    add_word_settings(stringf("PLL%d.CFG_%c.LOCK_DETECT_WIN", index, cfg), start + 77, 1);
    add_word_settings(stringf("PLL%d.CFG_%c.SYNC_BYPASS", index, cfg), start + 78, 1);
    add_word_settings(stringf("PLL%d.CFG_%c.FILTER_SHIFT", index, cfg), start + 79, 2);
    add_word_settings(stringf("PLL%d.CFG_%c.FAST_LOCK", index, cfg), start + 81, 1);
    add_word_settings(stringf("PLL%d.CFG_%c.SAR_LIMIT", index, cfg), start + 82, 3);
    add_word_settings(stringf("PLL%d.CFG_%c.OP_LOCK", index, cfg), start + 85, 1);
    add_word_settings(stringf("PLL%d.CFG_%c.PDIV1_SEL", index, cfg), start + 86, 1);
    add_word_settings(stringf("PLL%d.CFG_%c.PDIV0_MUX", index, cfg), start + 87, 1);
    add_word_settings(stringf("PLL%d.CFG_%c.EN_COARSE_TUNE", index, cfg), start + 88, 1);
    add_word_settings(stringf("PLL%d.CFG_%c.EN_USR_CFG", index, cfg), start + 89, 1);
    add_word_settings(stringf("PLL%d.CFG_%c.PLL_EN_SEL", index, cfg), start + 90, 1);
}

ConfigBitDatabase::ConfigBitDatabase() : BaseBitDatabase(Die::DIE_CONFIG_SIZE * 8)
{
    int pos = 0;
    for (int i = 0; i < 4; i++) {
        add_pll_cfg(i, 'A', pos);
        pos += 96;
        add_pll_cfg(i, 'B', pos);
        pos += 96;
    }

    // CLKIN matrix
    add_word_settings("CLKIN.REF0", pos + 0, 3);
    add_word_settings("CLKIN.REF0_INV", pos + 3, 1);
    add_word_settings("CLKIN.REF1", pos + 8, 3);
    add_word_settings("CLKIN.REF1_INV", pos + 8 + 3, 1);
    add_word_settings("CLKIN.REF2", pos + 16, 3);
    add_word_settings("CLKIN.REF2_INV", pos + 16 + 3, 1);
    add_word_settings("CLKIN.REF3", pos + 24, 3);
    add_word_settings("CLKIN.REF3_INV", pos + 24 + 3, 1);

    pos += 32;
    // GLBOUT matrix
    add_word_settings("GLBOUT.GLB0", pos + 0, 3);
    add_word_settings("GLBOUT.USR_GLB0", pos + 3, 1);
    add_word_settings("GLBOUT.GLB0_EN", pos + 4, 1);
    // bits 5-7 not used
    add_word_settings("GLBOUT.FB0", pos + 8, 2);
    add_word_settings("GLBOUT.USR_FB0", pos + 10, 1);
    // bits 11-15 not used
    add_word_settings("GLBOUT.GLB1", pos + 16, 3);
    add_word_settings("GLBOUT.USR_GLB1", pos + 19, 1);
    add_word_settings("GLBOUT.GLB1_EN", pos + 20, 1);
    // bits 21-23 not used
    add_word_settings("GLBOUT.FB1", pos + 24, 2);
    add_word_settings("GLBOUT.USR_FB1", pos + 26, 1);
    // bits 27-31 not used
    add_word_settings("GLBOUT.GLB2", pos + 32, 3);
    add_word_settings("GLBOUT.USR_GLB2", pos + 35, 1);
    add_word_settings("GLBOUT.GLB2_EN", pos + 36, 1);
    // bits 37-39 not used
    add_word_settings("GLBOUT.FB2", pos + 40, 2);
    add_word_settings("GLBOUT.USR_FB2", pos + 42, 1);
    // bits 43-47 not used
    add_word_settings("GLBOUT.GLB3", pos + 48, 3);
    add_word_settings("GLBOUT.USR_GLB3", pos + 51, 1);
    add_word_settings("GLBOUT.GLB3_EN", pos + 52, 1);
    // bits 53-55 not used
    add_word_settings("GLBOUT.FB3", pos + 56, 2);
    add_word_settings("GLBOUT.USR_FB3", pos + 58, 1);
    // bits 59-63 not used

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
        add_word_settings(stringf("PLL%d.PLL_RST", i), pos + 0, 1);
        add_word_settings(stringf("PLL%d.PLL_EN", i), pos + 1, 1);
        add_word_settings(stringf("PLL%d.PLL_AUTN", i), pos + 2, 1);
        add_word_settings(stringf("PLL%d.SET_SEL", i), pos + 3, 1);
        add_word_settings(stringf("PLL%d.USR_SET", i), pos + 4, 1);
        add_word_settings(stringf("PLL%d.USR_CLK_REF", i), pos + 5, 1);
        add_word_settings(stringf("PLL%d.CLK_OUT_EN", i), pos + 6, 1);
        add_word_settings(stringf("PLL%d.LOCK_REQ", i), pos + 7, 1);

        add_word_settings(stringf("PLL%d.AUTN_CT_I", i), pos + 8 + 0, 3);
        add_word_settings(stringf("PLL%d.CLK180_DOUB", i), pos + 8 + 3, 1);
        add_word_settings(stringf("PLL%d.CLK270_DOUB", i), pos + 8 + 4, 1);
        // bits 6 and 7 are unused
        add_word_settings(stringf("PLL%d.USR_CLK_OUT", i), pos + 8 + 7, 1);
        pos += 16;
    }
    add_unknowns();
}

std::vector<bool> WordSettingBits::get_value(const std::vector<bool> &tile) const
{
    std::vector<bool> val;
    for (int i = start; i < end; i++)
        val.push_back(tile[i]);
    return val;
}

void WordSettingBits::set_value(std::vector<bool> &tile, const std::vector<bool> &value) const
{
    for (int i = start; i < end; i++)
        tile[i] = value[i - start];
}

DatabaseConflictError::DatabaseConflictError(const std::string &desc) : runtime_error(desc) {}

} // namespace GateMate