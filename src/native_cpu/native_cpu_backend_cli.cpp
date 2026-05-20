#include "libreprimus/native_cpu/native_batch.hpp"

#include <cstdlib>
#include <exception>
#include <iostream>
#include <string>

namespace {

std::size_t parse_threads(int argc, char** argv) {
    std::size_t threads = 1;
    for (int index = 1; index < argc; ++index) {
        const std::string arg = argv[index];
        if ((arg == "--threads" || arg == "-t") && index + 1 < argc) {
            threads = static_cast<std::size_t>(std::stoul(argv[++index]));
        } else if (arg == "--help" || arg == "-h") {
            std::cout << "Usage: lpgpu_native_cpu_backend_cli --threads N\n";
            std::exit(0);
        }
    }
    return threads == 0 ? 1 : threads;
}

}  // namespace

int main(int argc, char** argv) {
    try {
        const auto threads = parse_threads(argc, argv);
        const auto run = libreprimus::native_cpu::run_stage5d_fixture(threads);
        std::cout << libreprimus::native_cpu::to_json(run);
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "native_cpu_backend_error=" << error.what() << '\n';
        return 1;
    }
}
