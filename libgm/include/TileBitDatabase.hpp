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

#ifndef LIBGATEMATE_TILEBITDATABASE_HPP
#define LIBGATEMATE_TILEBITDATABASE_HPP

#include <cstdint>
#include <map>
#include <string>
#include <vector>
#include "TileConfig.hpp"

namespace GateMate {

struct WordSettingBits
{
    int start;
    int end;
    vector<bool> get_value(const vector<bool> &tile) const;

    void set_value(vector<bool> &tile, const vector<bool> &value) const;

    inline bool operator==(const WordSettingBits &other) const { return (start == other.start) && (end == other.end); }
};

class BaseBitDatabase
{
  public:
    BaseBitDatabase();
    virtual ~BaseBitDatabase();

  protected:
    void add_word_settings(const std::string &name, int start, int end);
    std::vector<uint8_t> bits_to_bytes(std::vector<bool> &bits);

    map<std::string, WordSettingBits> words;
};

class TileBitDatabase : BaseBitDatabase
{
  public:
    TileBitDatabase(const int x, const int y);
    TileConfig tile_data_to_config(const vector<uint8_t> &data);
    std::vector<uint8_t> config_to_tile_data(const TileConfig &cfg);

  private:
    void add_sb_big(int index, int start);
    void add_sb_sml(int index, int start);
    void add_sb_drive(int index, int start);

    void add_cpe(int index, int start);
    void add_inmux(int index, int plane, int start);

    void add_gpio(int start);
    void add_edge_io(int index, int start);

    void add_right_edge(int index, int start);
    void add_left_edge(int index, int start);
    void add_top_edge(int index, int start);
    void add_bottom_edge(int index, int start);
};

class RamBitDatabase : BaseBitDatabase
{
  public:
    RamBitDatabase();
    TileConfig ram_data_to_config(const vector<uint8_t> &data);
    std::vector<uint8_t> config_to_ram_data(const TileConfig &cfg);
};

class DatabaseConflictError : public runtime_error
{
  public:
    explicit DatabaseConflictError(const string &desc);
};

} // namespace GateMate

#endif // LIBGATEMATE_TILEBITDATABASE_HPP
