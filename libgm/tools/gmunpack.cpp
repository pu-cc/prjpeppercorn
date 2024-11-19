#include "Chip.hpp"
#include "Bitstream.hpp"
#include "version.hpp"
#include <iostream>
#include <boost/optional.hpp>
#include <boost/program_options.hpp>
#include <boost/filesystem.hpp>
#include <stdexcept>
#include <streambuf>
#include <fstream>

using namespace std;

int main(int argc, char *argv[])
{
    using namespace GateMate;
    namespace po = boost::program_options;

    po::options_description options("Allowed options");
    options.add_options()("help,h", "show help");
    options.add_options()("verbose,v", "verbose output");
    po::positional_options_description pos;
    options.add_options()("input", po::value<std::string>()->required(), "input bitstream file");
    pos.add("input", 1);
    options.add_options()("textcfg", po::value<std::string>()->required(), "output textual configuration");
    pos.add("textcfg", 1);

    po::variables_map vm;
    try {
        po::parsed_options parsed = po::command_line_parser(argc, argv).options(options).positional(pos).run();
        po::store(parsed, vm);
        po::notify(vm);
    }
    catch (po::required_option &e) {
        cerr << "Error: input file is mandatory." << endl << endl;
        goto help;
    }
    catch (std::exception &e) {
        cerr << "Error: " << e.what() << endl << endl;
        goto help;
    }

    if (vm.count("help")) {
help:
        boost::filesystem::path path(argv[0]);
        cerr << "Open Source Tools for GateMate FPGAs Version " << git_describe_str << endl;
        cerr << "Copyright (C) 2024 YosysHQ GmbH" << endl;
        cerr << endl;
        cerr << path.stem().c_str() << ": GateMate bitstream to text config converter" << endl;
        cerr << endl;
        cerr << "Usage: " << argv[0] << " input.bit [output.config] [options]" << endl;
        cerr << endl;
        cerr << options << endl;
        return vm.count("help") ? 0 : 1;
    }

    ifstream bit_file(vm["input"].as<string>(), ios::binary);
    if (!bit_file) {
        cerr << "Failed to open input file" << endl;
        return 1;
    }

    try {
        Bitstream::read(bit_file).deserialise_chip();
        ofstream out_file(vm["textcfg"].as<string>());
        if (!out_file) {
            cerr << "Failed to open output file" << endl;
            return 1;
        }
        return 0;
    } catch (BitstreamParseError &e) {
        cerr << "Failed to process input bitstream: " << e.what() << endl;
        return 1;
    } catch (runtime_error &e) {
        cerr << "Failed to process input bitstream: " << e.what() << endl;
        return 1;
    }
}
