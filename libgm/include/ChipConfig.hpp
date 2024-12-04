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

#ifndef LIBGATEMATE_CHIPCONFIG_HPP
#define LIBGATEMATE_CHIPCONFIG_HPP

#include <cstdint>
#include <map>
#include <string>
#include <vector>
#include "TileConfig.hpp"

namespace GateMate {

class Chip;

struct CfgLoc
{
    int die;
    int x;
    int y;

    inline bool operator==(const CfgLoc &other) const { return other.die == die && other.x == x && other.y == y; }
    inline bool operator!=(const CfgLoc &other) const { return other.die != die || x != other.x || y == other.y; }

    inline bool operator<(const CfgLoc &other) const
    {
        return die < other.die ||
               ((die == other.die && y < other.y) || (die == other.die && y == other.y && x < other.x));
    }
};

class ChipConfig
{
  public:
    string chip_name;
    string chip_package;
    std::map<CfgLoc, TileConfig> tiles;
    std::map<CfgLoc, TileConfig> brams;

    // Block RAM initialisation
    std::map<CfgLoc, std::vector<uint8_t>> bram_data;

    std::string to_string() const;
    static ChipConfig from_string(const std::string &config);
    Chip to_chip() const;
    static ChipConfig from_chip(const Chip &chip);
};

} // namespace GateMate

#endif // LIBGATEMATE_CHIPCONFIG_HPP
