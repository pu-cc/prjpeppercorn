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
using namespace std;

namespace GateMate {

ostream &operator<<(ostream &out, const ConfigWord &cw)
{
    out << cw.name << " " << to_string(cw.value) << endl;
    return out;
}

istream &operator>>(istream &in, ConfigWord &cw)
{
    in >> cw.name;
    in >> cw.value;
    return in;
}

ostream &operator<<(ostream &out, const TileConfig &tc)
{
    for (const auto &cword : tc.cwords)
        out << cword;
    return out;
}

istream &operator>>(istream &in, TileConfig &tc)
{
    tc.cwords.clear();
    while (!skip_check_eor(in)) {
        ConfigWord w;
        in >> w;
        tc.cwords.push_back(w);
    }
    return in;
}

void TileConfig::add_word(const string &name, const vector<bool> &value) { cwords.push_back({name, value}); }

string TileConfig::to_string() const
{
    stringstream ss;
    ss << *this;
    return ss.str();
}

TileConfig TileConfig::from_string(const string &str)
{
    stringstream ss(str);
    TileConfig tc;
    ss >> tc;
    return tc;
}

bool TileConfig::empty() const { return cwords.empty(); }

} // namespace GateMate
