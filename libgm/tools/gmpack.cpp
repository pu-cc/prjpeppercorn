#include "Bitstream.hpp"
#include "Chip.hpp"
#include "version.hpp"
#include <iostream>
#include <boost/program_options.hpp>
#include <boost/filesystem.hpp>
#include <stdexcept>
#include <streambuf>
#include <fstream>
#include <iomanip>

using namespace std;

int main(int argc, char *argv[])
{
    using namespace GateMate;
    namespace po = boost::program_options;

    po::options_description options("Allowed options");
    options.add_options()("help,h", "show help");
    options.add_options()("verbose,v", "verbose output");
    po::positional_options_description pos;
    options.add_options()("input", po::value<std::string>()->required(), "input textual configuration");
    pos.add("input", 1);
    options.add_options()("bit", po::value<std::string>(), "output bitstream file");
    pos.add("bit", 1);

    po::variables_map vm;

    try {
        po::parsed_options parsed = po::command_line_parser(argc, argv).options(options).positional(pos).run();
        po::store(parsed, vm);
        po::notify(vm);
    }
    catch (po::required_option& e) {
        cerr << "Error: input file is mandatory." << endl << endl;
        goto help;
    }
    catch (std::exception& e) {
        cerr << "Error: " << e.what() << endl << endl;
        goto help;
    }

    if (vm.count("help")) {
help:
        boost::filesystem::path path(argv[0]);
        cerr << "Open Source Tools for GateMate FPGAs Version " << git_describe_str << endl;
        cerr << "Copyright (C) 2024 YosysHQ GmbH" << endl;
        cerr << endl;
        cerr << path.stem().c_str() << ": GateMate bitstream packer" << endl;
        cerr << endl;
        cerr << "Usage: " << argv[0] << " input.config [output.bit] [options]" << endl;
        cerr << endl;
        cerr << options << endl;
        return vm.count("help") ? 0 : 1;
    }

    ifstream config_file(vm["input"].as<string>());
    if (!config_file) {
        cerr << "Failed to open input file" << endl;
        return 1;
    }

    string textcfg((std::istreambuf_iterator<char>(config_file)), std::istreambuf_iterator<char>());
    Chip c;
    Bitstream b = Bitstream::serialise_chip(c);
    if (vm.count("bit")) {
        ofstream bit_file(vm["bit"].as<string>(), ios::binary);
        if (!bit_file) {
            cerr << "Failed to open output file" << endl;
            return 1;
        }
        b.write_bit(bit_file);
    }     
    return 0;
}
