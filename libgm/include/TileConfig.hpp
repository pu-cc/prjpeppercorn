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

#ifndef LIBGATEMATE_TILECONFIG_HPP
#define LIBGATEMATE_TILECONFIG_HPP

#include <cstdint>
#include <iostream>
#include <map>
#include <string>
#include <vector>

namespace GateMate {

struct ConfigWord
{
    std::string name;
    std::vector<bool> value;
    inline bool operator==(const ConfigWord &other) const { return other.name == name && other.value == value; }
};

std::ostream &operator<<(std::ostream &out, const ConfigWord &cw);

std::istream &operator>>(std::istream &in, ConfigWord &cw);

struct TileConfig
{
    std::vector<ConfigWord> cwords;
    int total_known_bits = 0;

    void add_word(const std::string &name, const std::vector<bool> &value);

    std::string to_string() const;
    static TileConfig from_string(const std::string &str);

    bool empty() const;
};

std::ostream &operator<<(std::ostream &out, const TileConfig &tc);

std::istream &operator>>(std::istream &in, TileConfig &ce);

} // namespace GateMate

#endif // LIBGATEMATE_TILECONFIG_HPP
