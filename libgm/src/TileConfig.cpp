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

#include "TileConfig.hpp"
#include <algorithm>
#include <sstream>
#include "Util.hpp"

namespace GateMate {

std::ostream &operator<<(std::ostream &out, const ConfigWord &cw)
{
    out << cw.name << " " << to_string(cw.value) << std::endl;
    return out;
}

std::istream &operator>>(std::istream &in, ConfigWord &cw)
{
    in >> cw.name;
    in >> cw.value;
    return in;
}

std::ostream &operator<<(std::ostream &out, const TileConfig &tc)
{
    for (const auto &cword : tc.cwords)
        out << cword;
    return out;
}

std::istream &operator>>(std::istream &in, TileConfig &tc)
{
    tc.cwords.clear();
    while (!skip_check_eor(in)) {
        ConfigWord w;
        in >> w;
        tc.cwords.push_back(w);
    }
    return in;
}

void TileConfig::add_word(const std::string &name, const std::vector<bool> &value) { cwords.push_back({name, value}); }

std::string TileConfig::to_string() const
{
    std::stringstream ss;
    ss << *this;
    return ss.str();
}

TileConfig TileConfig::from_string(const std::string &str)
{
    std::stringstream ss(str);
    TileConfig tc;
    ss >> tc;
    return tc;
}

bool TileConfig::empty() const { return cwords.empty(); }

} // namespace GateMate
