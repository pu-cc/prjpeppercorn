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

#include "Bitstream.hpp"
#include <bitset>
#include <boost/algorithm/string/predicate.hpp>
#include <boost/optional.hpp>
#include <cstring>
#include <iostream>
#include "Chip.hpp"
#include "Util.hpp"

namespace GateMate {

static constexpr const uint8_t CMD_PLL = 0xc1;
static constexpr const uint8_t CMD_CFGMODE = 0xc2;
static constexpr const uint8_t CMD_CFGRST = 0xc3; //
static constexpr const uint8_t CMD_FLASH = 0xc5;
static constexpr const uint8_t CMD_DLXP = 0xc6; //
static constexpr const uint8_t CMD_DLYP = 0xc7; //
static constexpr const uint8_t CMD_LXLYS = 0xc8;
static constexpr const uint8_t CMD_ACLCU = 0xc9;
static constexpr const uint8_t CMD_DLCU = 0xca;
static constexpr const uint8_t CMD_DRXP = 0xcc; //
static constexpr const uint8_t CMD_RXRYS = 0xce;
static constexpr const uint8_t CMD_FRAM = 0xd2;
static constexpr const uint8_t CMD_SERDES = 0xd7; //
static constexpr const uint8_t CMD_D2D = 0xd8;    //
static constexpr const uint8_t CMD_PATH = 0xd9;
static constexpr const uint8_t CMD_JUMP = 0xda; //
static constexpr const uint8_t CMD_CHG_STATUS = 0xdb;
static constexpr const uint8_t CMD_WAIT_PLL = 0xdc; //
static constexpr const uint8_t CMD_SPLL = 0xdd;
static constexpr const uint8_t CMD_SLAVE_MODE = 0xde;

static const uint16_t crc_table_x25[256] = {
        0x0000, 0x1189, 0x2312, 0x329b, 0x4624, 0x57ad, 0x6536, 0x74bf, 0x8c48, 0x9dc1, 0xaf5a, 0xbed3, 0xca6c, 0xdbe5,
        0xe97e, 0xf8f7, 0x1081, 0x0108, 0x3393, 0x221a, 0x56a5, 0x472c, 0x75b7, 0x643e, 0x9cc9, 0x8d40, 0xbfdb, 0xae52,
        0xdaed, 0xcb64, 0xf9ff, 0xe876, 0x2102, 0x308b, 0x0210, 0x1399, 0x6726, 0x76af, 0x4434, 0x55bd, 0xad4a, 0xbcc3,
        0x8e58, 0x9fd1, 0xeb6e, 0xfae7, 0xc87c, 0xd9f5, 0x3183, 0x200a, 0x1291, 0x0318, 0x77a7, 0x662e, 0x54b5, 0x453c,
        0xbdcb, 0xac42, 0x9ed9, 0x8f50, 0xfbef, 0xea66, 0xd8fd, 0xc974, 0x4204, 0x538d, 0x6116, 0x709f, 0x0420, 0x15a9,
        0x2732, 0x36bb, 0xce4c, 0xdfc5, 0xed5e, 0xfcd7, 0x8868, 0x99e1, 0xab7a, 0xbaf3, 0x5285, 0x430c, 0x7197, 0x601e,
        0x14a1, 0x0528, 0x37b3, 0x263a, 0xdecd, 0xcf44, 0xfddf, 0xec56, 0x98e9, 0x8960, 0xbbfb, 0xaa72, 0x6306, 0x728f,
        0x4014, 0x519d, 0x2522, 0x34ab, 0x0630, 0x17b9, 0xef4e, 0xfec7, 0xcc5c, 0xddd5, 0xa96a, 0xb8e3, 0x8a78, 0x9bf1,
        0x7387, 0x620e, 0x5095, 0x411c, 0x35a3, 0x242a, 0x16b1, 0x0738, 0xffcf, 0xee46, 0xdcdd, 0xcd54, 0xb9eb, 0xa862,
        0x9af9, 0x8b70, 0x8408, 0x9581, 0xa71a, 0xb693, 0xc22c, 0xd3a5, 0xe13e, 0xf0b7, 0x0840, 0x19c9, 0x2b52, 0x3adb,
        0x4e64, 0x5fed, 0x6d76, 0x7cff, 0x9489, 0x8500, 0xb79b, 0xa612, 0xd2ad, 0xc324, 0xf1bf, 0xe036, 0x18c1, 0x0948,
        0x3bd3, 0x2a5a, 0x5ee5, 0x4f6c, 0x7df7, 0x6c7e, 0xa50a, 0xb483, 0x8618, 0x9791, 0xe32e, 0xf2a7, 0xc03c, 0xd1b5,
        0x2942, 0x38cb, 0x0a50, 0x1bd9, 0x6f66, 0x7eef, 0x4c74, 0x5dfd, 0xb58b, 0xa402, 0x9699, 0x8710, 0xf3af, 0xe226,
        0xd0bd, 0xc134, 0x39c3, 0x284a, 0x1ad1, 0x0b58, 0x7fe7, 0x6e6e, 0x5cf5, 0x4d7c, 0xc60c, 0xd785, 0xe51e, 0xf497,
        0x8028, 0x91a1, 0xa33a, 0xb2b3, 0x4a44, 0x5bcd, 0x6956, 0x78df, 0x0c60, 0x1de9, 0x2f72, 0x3efb, 0xd68d, 0xc704,
        0xf59f, 0xe416, 0x90a9, 0x8120, 0xb3bb, 0xa232, 0x5ac5, 0x4b4c, 0x79d7, 0x685e, 0x1ce1, 0x0d68, 0x3ff3, 0x2e7a,
        0xe70e, 0xf687, 0xc41c, 0xd595, 0xa12a, 0xb0a3, 0x8238, 0x93b1, 0x6b46, 0x7acf, 0x4854, 0x59dd, 0x2d62, 0x3ceb,
        0x0e70, 0x1ff9, 0xf78f, 0xe606, 0xd49d, 0xc514, 0xb1ab, 0xa022, 0x92b9, 0x8330, 0x7bc7, 0x6a4e, 0x58d5, 0x495c,
        0x3de3, 0x2c6a, 0x1ef1, 0x0f78};

class Crc16
{
  public:
    uint16_t crc16 = 0xFFFF;

    void update_crc16(uint8_t val) { crc16 = (crc16 >> 8) ^ crc_table_x25[(crc16 & 0xFF) ^ val]; }

    uint16_t get_crc16() { return crc16 ^ 0xFFFF; }

    void reset_crc16() { crc16 = 0xFFFF; }
};

// The BitstreamReadWriter class stores state (including CRC16) whilst reading
// the bitstream
class BitstreamReadWriter
{
  public:
    BitstreamReadWriter() : data(), iter(data.begin()) {};

    BitstreamReadWriter(const vector<uint8_t> &data) : data(data), iter(this->data.begin()) {};

    vector<uint8_t> data;
    vector<uint8_t>::iterator iter;
    Crc16 crc16;

    // Return a single byte and update CRC
    inline uint8_t get_byte()
    {
        assert(iter < data.end());
        uint8_t val = *(iter++);
        crc16.update_crc16(val);
        return val;
    }

    // Read a little endian uint16 from the bitstream and update CRC
    uint16_t get_uint16()
    {
        uint8_t tmp[2];
        get_bytes(tmp, 2);
        return (tmp[0] << 8UL) | (tmp[1]);
    }

    // Read a little endian uint32 from the bitstream and update CRC
    uint32_t get_uint32()
    {
        uint8_t tmp[4];
        get_bytes(tmp, 4);
        return (tmp[0] << 24UL) | (tmp[1] << 16UL) | (tmp[2] << 8UL) | (tmp[3]);
    }

    // CRC is in big endian order
    uint16_t get_crc()
    {
        uint8_t tmp[2];
        get_bytes(tmp, 2);
        return (tmp[1] << 8UL) | (tmp[0]);
    }

    // The command opcode is a byte so this works like get_byte
    inline uint8_t get_command_opcode()
    {
        assert(iter < data.end());
        uint8_t val = *(iter++);
        crc16.update_crc16(val);
        return val;
    }

    // Write a single byte and update CRC
    inline void write_byte(uint8_t b)
    {
        data.push_back(b);
        crc16.update_crc16(b);
    }

    // Copy multiple bytes into an OutputIterator and update CRC
    template <typename T> void get_bytes(T out, size_t count)
    {
        for (size_t i = 0; i < count; i++) {
            *out = get_byte();
            ++out;
        }
    }

    void get_vector(std::vector<uint8_t> &out, size_t count)
    {
        for (size_t i = 0; i < count; i++) {
            out.push_back(get_byte());
        }
    }

    // Write multiple bytes from an InputIterator and update CRC
    template <typename T> void write_bytes(T in, size_t count)
    {
        for (size_t i = 0; i < count; i++)
            write_byte(*(in++));
    }

    void write_bytes(std::vector<uint8_t> in)
    {
        for (auto val : in)
            write_byte(val);
    }

    // Skip over bytes while updating CRC
    void skip_bytes(size_t count)
    {
        for (size_t i = 0; i < count; i++)
            get_byte();
    }

    // Write a little endian uint16_t into the bitstream
    void write_uint16(uint16_t val)
    {
        write_byte(uint8_t((val >> 8UL) & 0xFF));
        write_byte(uint8_t(val & 0xFF));
    }

    // Write a little endian uint32_t into the bitstream
    void write_uint32(uint32_t val)
    {
        write_byte(uint8_t((val >> 24UL) & 0xFF));
        write_byte(uint8_t((val >> 16UL) & 0xFF));
        write_byte(uint8_t((val >> 8UL) & 0xFF));
        write_byte(uint8_t(val & 0xFF));
    }

    // Get the offset into the bitstream
    size_t get_offset() { return size_t(distance(data.begin(), iter)); }

    // Check the calculated CRC16 against an actual CRC16, expected in the next 2
    // bytes
    void check_crc16()
    {
        uint8_t crc_bytes[2];
        uint16_t actual_crc = crc16.get_crc16();
        get_bytes(crc_bytes, 2);
        // cerr << hex << int(crc_bytes[0]) << " " << int(crc_bytes[1]) << endl;
        uint16_t exp_crc = (crc_bytes[0] << 8) | crc_bytes[1];
        if (actual_crc != exp_crc) {
            ostringstream err;
            err << "crc fail, calculated 0x" << hex << actual_crc << " but expecting 0x" << exp_crc;
            throw BitstreamParseError(err.str(), get_offset());
        }
        crc16.reset_crc16();
    }

    // Insert the calculated CRC16 into the bitstream
    void insert_crc16()
    {
        uint16_t actual_crc = crc16.get_crc16();
        write_byte(uint8_t((actual_crc) & 0xFF));
        write_byte(uint8_t((actual_crc >> 8) & 0xFF));
    }

    bool is_end() { return (iter >= data.end()); }

    const vector<uint8_t> &get() { return data; };

    void write_nops(size_t count)
    {
        for (size_t i = 0; i < count; i++)
            write_byte(0);
    }

    // Writing commands
    void write_header(uint8_t cmd, uint16_t len)
    {
        crc16.reset_crc16();
        write_byte(cmd);
        if (len == CMD_FRAM)
            write_uint16(len);
        else
            write_byte(len & 0xff);
        insert_crc16();
    }

    void write_cmd_path(uint8_t data)
    {
        write_header(CMD_PATH, 1);
        write_byte(data);
        insert_crc16();
        write_nops(4);
        write_byte(0x33);
        write_nops(4);
    }

    void write_cmd_spll(uint8_t data)
    {
        write_header(CMD_SPLL, 1);
        write_byte(data);
        insert_crc16();
    }

    void write_cmd_wait_pll(uint8_t data)
    {
        write_header(CMD_WAIT_PLL, 1);
        write_byte(data);
        insert_crc16();
    }

    void write_cmd_cfgrst(uint8_t data)
    {
        write_header(CMD_CFGRST, 1);
        write_byte(data);
        insert_crc16();
    }

    void write_cmd_slave_mode(uint8_t data)
    {
        write_header(CMD_SLAVE_MODE, 1);
        write_byte(data);
        insert_crc16();
        write_nops(3);
    }

    void write_cmd_d2d(uint8_t data)
    {
        write_header(CMD_D2D, 1);
        write_byte(data);
        insert_crc16();
    }

    void write_cmd_rxrys(uint8_t x_ram_sel, uint8_t y_ram_sel)
    {
        write_header(CMD_RXRYS, 2);
        write_byte(x_ram_sel);
        write_byte(y_ram_sel);
        insert_crc16();
    }

    void write_cmd_lxlys(uint8_t x_sel, uint8_t y_sel)
    {
        write_header(CMD_LXLYS, 2);
        write_byte(x_sel);
        write_byte(y_sel);
        insert_crc16();
    }

    void write_cmd_aclcu(uint16_t data)
    {
        write_header(CMD_ACLCU, 2);
        write_uint16(data);
        insert_crc16();
    }

    void write_cmd_pll_empty()
    {
        write_header(CMD_PLL, 12);
        for (int i = 0; i < 12; i++)
            write_byte(0);
        insert_crc16();
        write_nops(6);
    }

    void write_cmd_pll(int index, std::vector<uint8_t> data, int size)
    {
        write_header(CMD_PLL, size);
        for (int i = 0; i < Die::PLL_CFG_SIZE; i++)
            write_byte(data[i + index * Die::PLL_CFG_SIZE]);
        int pos = Die::PLL_CFG_SIZE * Die::MAX_PLL * 2;
        for (int i = pos; i < pos + size - Die::PLL_CFG_SIZE; i++)
            write_byte(data[i]);
        insert_crc16();
        write_nops(6);
    }
};

void check_crc(BitstreamReadWriter &rd)
{
    uint16_t actual_crc = rd.crc16.get_crc16();
    uint16_t exp_crc = rd.get_crc(); // crc
    if (actual_crc != exp_crc) {
        ostringstream err;
        err << "crc fail, calculated 0x" << hex << actual_crc << " but expecting 0x" << exp_crc;
        throw BitstreamParseError(err.str());
    }
}

#define BITSTREAM_DEBUG(x)                                                                                             \
    if (verbosity >= VerbosityLevel::DEBUG)                                                                            \
    cerr << "bitstream: " << x << endl
#define BITSTREAM_NOTE(x)                                                                                              \
    if (verbosity >= VerbosityLevel::NOTE)                                                                             \
    cerr << "bitstream: " << x << endl
#define BITSTREAM_FATAL(x, pos)                                                                                        \
    {                                                                                                                  \
        ostringstream ss;                                                                                              \
        ss << x;                                                                                                       \
        throw BitstreamParseError(ss.str(), pos);                                                                      \
    }

Bitstream::Bitstream(const std::vector<uint8_t> &data) : data(data) {}

Bitstream Bitstream::read(std::istream &in)
{
    std::vector<uint8_t> bytes;
    in.seekg(0, in.end);
    size_t length = size_t(in.tellg());
    in.seekg(0, in.beg);
    bytes.resize(length);
    in.read(reinterpret_cast<char *>(&(bytes[0])), length);
    return Bitstream(bytes);
}

Chip Bitstream::deserialise_chip()
{
    cerr << "bitstream size: " << data.size() * 8 << " bits" << endl;
    Chip chip(1);
    Die &die = chip.get_die(0);

    BitstreamReadWriter rd(data);
    bool is_block_ram = false;
    uint8_t x_pos = 0, y_pos = 0;
    uint8_t pll_select = 0x0f;
    uint16_t aclcu = 0;
    std::map<std::pair<int, int>, int> tile_iteration;
    while (!rd.is_end()) {
        rd.crc16.reset_crc16();
        uint8_t cmd = rd.get_command_opcode();
        uint16_t length = (cmd == CMD_FRAM) ? rd.get_uint16() : rd.get_byte();
        std::vector<uint8_t> block;
        switch (cmd) {
        case CMD_DLCU:
            BITSTREAM_DEBUG("CMD_DLCU");
            // if (length>112)
            //     BITSTREAM_FATAL("DLCU data longer than expected", rd.get_offset());
            if (is_block_ram) {
                if (length > 27)
                    BITSTREAM_FATAL("RAM configuration must be up to 27 bytes", rd.get_offset());
            } else {
                if (length > 112)
                    BITSTREAM_FATAL("Tile configuration must be up to 112 bytes", rd.get_offset());
            }
            // Check header CRC
            check_crc(rd);

            // Read data block
            rd.get_vector(block, length);
            // Check data CRC
            check_crc(rd);

            if (is_block_ram)
                die.write_ram(x_pos, y_pos, block);
            else {
                int iteration = -1;
                if (tile_iteration.count(std::make_pair(x_pos, y_pos)))
                    iteration = tile_iteration[std::make_pair(x_pos, y_pos)];
                tile_iteration[std::make_pair(x_pos, y_pos)] = ++iteration;

                // Detection of FF initialization is possible on
                // last iteration
                if (iteration == 2) {
                    std::vector<uint8_t> data = die.get_latch_config(x_pos, y_pos);
                    // Make sure we have CPE data
                    // even if uninitialized
                    block.resize(40, 0x00);
                    uint8_t val = 0x00;
                    for (int i = 0; i < 4; i++) {
                        uint8_t v = block[i * 10 + 8] ^ data[i * 10 + 8];
                        if (v == 0x30)
                            val |= Die::FF_INIT_RESET << (i * 2);
                        else if (v == 0xc0)
                            val |= Die::FF_INIT_SET << (i * 2);
                        else if (v != 0x00)
                            BITSTREAM_FATAL(stringf("Unknown CPE state %d on pos %d,%d\n", v, x_pos, y_pos),
                                            rd.get_offset());
                    }
                    die.write_ff_init(x_pos, y_pos, val);
                }
                die.write_latch(x_pos, y_pos, block);
            }
            break;
        case CMD_PATH:
            BITSTREAM_DEBUG("CMD_PATH");
            if (length != 1)
                BITSTREAM_FATAL("PATH data must be one byte long", rd.get_offset());
            // Check header CRC
            check_crc(rd);
            // Read data block
            rd.get_byte();
            // Check data CRC
            check_crc(rd);

            // Skip bytes
            rd.skip_bytes(9);
            break;
        case CMD_SPLL:
            BITSTREAM_DEBUG("CMD_SPLL");
            if (length != 1)
                BITSTREAM_FATAL("SPLL data must be one byte long", rd.get_offset());
            // Check header CRC
            check_crc(rd);
            // Read data block
            pll_select = rd.get_byte();
            // Check data CRC
            check_crc(rd);
            break;
        case CMD_PLL:
            BITSTREAM_DEBUG("CMD_PLL");
            if (length < 12)
                BITSTREAM_FATAL("PLL data smaller than expected", rd.get_offset());
            if (length > 24)
                BITSTREAM_FATAL("PLL data longer than expected", rd.get_offset());
            // Check header CRC
            check_crc(rd);

            // Read data block
            rd.get_vector(block, length);
            die.write_pll_select(pll_select, block);
            // Check data CRC
            check_crc(rd);

            // Skip bytes
            rd.skip_bytes(6);
            break;
        case CMD_LXLYS:
            if (length != 2)
                BITSTREAM_FATAL("LXLYS data must be two bytes long", rd.get_offset());
            // Check header CRC
            check_crc(rd);

            BITSTREAM_DEBUG("CMD_LXLYS");
            is_block_ram = false;
            x_pos = rd.get_byte();
            if (x_pos > 81)
                BITSTREAM_FATAL("Tile column (X) must be in range 0-81, current value " << x_pos, rd.get_offset());
            y_pos = rd.get_byte();
            if (y_pos > 65)
                BITSTREAM_FATAL("Tile row (Y) must be in range 0-65, current value " << y_pos, rd.get_offset());
            // Check data CRC
            check_crc(rd);
            break;
        case CMD_ACLCU:
            BITSTREAM_DEBUG("CMD_ACLCU");
            if (length != 2)
                BITSTREAM_FATAL("ACLCU data must be two bytes long", rd.get_offset());
            // Check header CRC
            check_crc(rd);
            aclcu = rd.get_uint16();
            // Check data CRC
            check_crc(rd);
            break;
        case CMD_RXRYS:
            BITSTREAM_DEBUG("CMD_RXRYS");
            if (length != 2)
                BITSTREAM_FATAL("RXRYS data must be two bytes long", rd.get_offset());
            // Check header CRC
            check_crc(rd);
            is_block_ram = true;

            x_pos = rd.get_byte();
            if (x_pos > 3)
                BITSTREAM_FATAL("RAM column (X) must be in range 0-3, current value " << x_pos, rd.get_offset());
            y_pos = rd.get_byte();
            if (y_pos > 7)
                BITSTREAM_FATAL("RAM row (Y) must be in range 0-7, current value " << y_pos, rd.get_offset());
            // Check data CRC
            check_crc(rd);
            break;
        case CMD_FRAM:
            BITSTREAM_DEBUG("CMD_FRAM");
            if (length > 5120)
                BITSTREAM_FATAL("FRAM data longer than expected", rd.get_offset());
            // Check header CRC
            check_crc(rd);

            // Read data block
            rd.get_vector(block, length);
            // Check data CRC
            check_crc(rd);

            die.write_ram_data(x_pos, y_pos, block, aclcu);
            break;
        case CMD_CHG_STATUS:
            BITSTREAM_DEBUG("CMD_CHG_STATUS");
            if (length > 12)
                BITSTREAM_FATAL("CHG_STATUS data longer than expected", rd.get_offset());
            // Check header CRC
            check_crc(rd);

            // Read data block
            rd.get_vector(block, length);
            // Check data CRC
            check_crc(rd);

            // Skip bytes
            rd.skip_bytes(9);
            break;
        case CMD_SLAVE_MODE:
            BITSTREAM_DEBUG("CMD_SLAVE_MODE");
            if (length > 1)
                BITSTREAM_FATAL("SLAVE_MODE must be one byte long", rd.get_offset());
            // Check header CRC
            check_crc(rd);

            // Read data block
            rd.get_byte();
            // Check data CRC
            check_crc(rd);

            // Skip bytes
            rd.skip_bytes(3);
            break;
        case CMD_FLASH:
            BITSTREAM_DEBUG("CMD_FLASH");
            if (length > 11)
                BITSTREAM_FATAL("FLASH data longer than expected", rd.get_offset());
            // Check header CRC
            check_crc(rd);

            // Read data block
            rd.get_vector(block, length);
            // Check data CRC
            check_crc(rd);
            break;
        case CMD_CFGMODE:
            BITSTREAM_DEBUG("CMD_CFGMODE");
            if (length > 20)
                BITSTREAM_FATAL("PLL data longer than expected", rd.get_offset());
            // Check header CRC
            check_crc(rd);

            // Read data block
            rd.get_vector(block, length);
            // Check data CRC
            check_crc(rd);

            // Skip bytes
            rd.skip_bytes(3);
            break;
        default:
            BITSTREAM_FATAL("Unhandled command 0x" << hex << setw(2) << setfill('0') << int(cmd), rd.get_offset());
            break;
        }
    }
    return chip;
}

bool is_edge_location(int x, int y)
{
    return ((x == 0) || (x == Die::MAX_COLS - 1) || (y == 0) || (y == Die::MAX_ROWS - 1));
}

Bitstream Bitstream::serialise_chip(const Chip &chip)
{
    BitstreamReadWriter wr;
    wr.write_cmd_path(0x10);
    auto &die = chip.get_die(0);
    std::vector<uint8_t> pll_data = die.get_pll_config();
    bool pll_written = false;
    for (int i = 0; i < Die::MAX_PLL; i++) {
        bool cfg_a = !die.is_pll_cfg_empty(i * 2 + 0);
        bool cfg_b = !die.is_pll_cfg_empty(i * 2 + 1);
        int size = Die::PLL_CFG_SIZE;
        if (!die.is_clkin_cfg_empty())
            size = Die::PLL_CFG_SIZE + Die::CLKIN_CFG_SIZE;
        if (!die.is_glbout_cfg_empty())
            size = Die::PLL_CFG_SIZE + Die::CLKIN_CFG_SIZE + Die::GLBOUT_CFG_SIZE;
        if (cfg_a || cfg_b) {
            wr.write_cmd_spll(1 << i);
            wr.write_cmd_pll(i * 2, pll_data, size);
            if (cfg_b) {
                wr.write_cmd_spll(1 << i | 1 << (i + 4));
                wr.write_cmd_pll(i * 2, pll_data, size);
            }
            pll_written = true;
        }
    }
    if (!pll_written)
        wr.write_cmd_pll_empty();

    for (int iteration = 0; iteration < 3; iteration++) {
        for (int y = 0; y < Die::MAX_ROWS; y++) {
            for (int x = 0; x < Die::MAX_COLS; x++) {
                // Empty configuration is skipped
                if (die.is_latch_empty(x, y))
                    continue;
                // Only tiles with CPE can have multiple iterations
                if (iteration != 0 && is_edge_location(x, y))
                    continue;
                // If CPE empty skip other iterations
                if (iteration != 0 && die.is_cpe_empty(x, y))
                    continue;
                std::vector<uint8_t> data = std::vector<uint8_t>(die.get_latch_config(x, y));
                uint8_t ff_init = data.back();
                data.pop_back();
                if (!is_edge_location(x, y)) {
                    if (iteration == 0) {
                        // First iteration does not setup CPE at all
                        std::fill(data.begin(), data.begin() + 40, 0);
                        // Empty configuration is skipped
                        if (std::all_of(data.begin(), data.end(), [](uint8_t i) { return i == 0; }))
                            continue;
                    }
                    // 2nd iteration with no changes if no FF initialization
                    if (iteration == 1 && ff_init) {
                        // Only CPE data is exported
                        data.resize(40);
                        // Set initial FFs states
                        for (int i = 0; i < 4; i++) {
                            uint8_t ff = (ff_init >> (i * 2)) & 0x03;
                            if (ff == Die::FF_INIT_RESET)
                                data[i * 10 + 8] &= 0x30 ^ 0xff;
                            else if (ff == Die::FF_INIT_SET)
                                data[i * 10 + 8] &= 0xc0 ^ 0xff;
                        }
                    }
                    // 3rd iteration only if there was FF initialization
                    if (iteration == 2) {
                        if (!ff_init)
                            continue;
                        // Only CPE data is exported
                        data.resize(40);
                    }
                }
                // minimize output
                auto rit = std::find_if(data.rbegin(), data.rend(), [](uint8_t val) { return val != 0; });
                data.erase(rit.base(), end(data));

                wr.write_cmd_lxlys(x, y);
                wr.write_header(CMD_DLCU, data.size());
                wr.write_bytes(data);
                wr.insert_crc16();
            }
        }
    }
    wr.write_header(CMD_CHG_STATUS, 12);
    wr.write_byte(0x13); // 0
    wr.write_byte(0x00); // 1
    wr.write_byte(0x33); // 2
    wr.write_byte(0x33); // 3
    wr.write_byte(0x00); // 4
    wr.write_byte(0x00); // 5
    wr.write_byte(0x00); // 6
    wr.write_byte(0x00); // 7
    wr.write_byte(0x00); // 8
    wr.write_byte(0x00); // 9
    wr.write_byte(0x00); // 10
    wr.write_byte(0x00); // 11
    wr.insert_crc16();
    wr.write_nops(4);
    wr.write_byte(0x33);
    wr.write_nops(4);
    return Bitstream(wr.get());
}

void Bitstream::write_bit(std::ostream &out)
{
    // Dump raw bitstream
    out.write(reinterpret_cast<const char *>(&(data[0])), data.size());
}

BitstreamParseError::BitstreamParseError(const std::string &desc) : runtime_error(desc.c_str()), desc(desc), offset(-1)
{
}

BitstreamParseError::BitstreamParseError(const std::string &desc, size_t offset)
        : runtime_error(desc.c_str()), desc(desc), offset(int(offset))
{
}

const char *BitstreamParseError::what() const noexcept
{
    std::ostringstream ss;
    ss << "Bitstream Parse Error: ";
    ss << desc;
    if (offset != -1)
        ss << " [at 0x" << std::hex << setw(8) << setfill('0') << offset << "]";
    return strdup(ss.str().c_str());
}
} // namespace GateMate
