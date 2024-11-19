#ifndef LIBGATEMATE_BITSTREAM_HPP
#define LIBGATEMATE_BITSTREAM_HPP

#include <cstdint>
#include <memory>
#include <iostream>


#include <vector>
#include <string>
#include <stdexcept>
#include <map>
#include <boost/optional.hpp>

namespace GateMate {

class Chip;

class Bitstream
{
  public:
    static Bitstream read(std::istream &in);
    // Serialise a Chip back to a bitstream
    static Bitstream serialise_chip(const Chip &chip);

    // Deserialise a bitstream to a Chip
    Chip deserialise_chip();

    void write_bit(std::ostream &out);
  private:
    Bitstream(const std::vector<uint8_t> &data);

    // Bitstream raw data
    std::vector<uint8_t> data;
};

class BitstreamParseError : std::runtime_error
{
  public:
    explicit BitstreamParseError(const std::string &desc);

    BitstreamParseError(const std::string &desc, size_t offset);

    const char *what() const noexcept override;

  private:
    std::string desc;
    int offset;
};
} // namespace GateMate
#endif // LIBGATEMATE_BITSTREAM_HPP
