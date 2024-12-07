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
    BaseBitDatabase(int num_bits);
    virtual ~BaseBitDatabase();

    TileConfig data_to_config(const vector<uint8_t> &data);
    std::vector<uint8_t> config_to_data(const TileConfig &cfg);

  protected:
    void add_word_settings(const std::string &name, int start, int end);
    void add_unknowns();
    std::vector<uint8_t> bits_to_bytes(std::vector<bool> &bits);

    int num_bits;
    map<std::string, WordSettingBits> words;
    std::vector<uint8_t> known_bits;
};

class TileBitDatabase : public BaseBitDatabase
{
  public:
    TileBitDatabase(const int x, const int y);

  private:
    void add_sb_big(int index, int start);
    void add_sb_sml(int index, int start);
    void add_sb_drive(int index, int start);

    void add_cpe(int index, int start);
    void add_ff_init(int index, int start);
    void add_inmux(int index, int plane, int start);

    void add_gpio(int start);
    void add_edge_io(int index, int start);

    void add_right_edge(int index, int start);
    void add_left_edge(int index, int start);
    void add_top_edge(int index, int start);
    void add_bottom_edge(int index, int start);
};

class RamBitDatabase : public BaseBitDatabase
{
  public:
    RamBitDatabase();
};

class ConfigBitDatabase : public BaseBitDatabase
{
  public:
    ConfigBitDatabase();
};

class DatabaseConflictError : public runtime_error
{
  public:
    explicit DatabaseConflictError(const string &desc);
};

} // namespace GateMate

#endif // LIBGATEMATE_TILEBITDATABASE_HPP
