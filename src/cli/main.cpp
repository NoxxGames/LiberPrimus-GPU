#include <iostream>

#include "libreprimus/build_config.hpp"
#include "libreprimus/version.hpp"

int main() {
    std::cout << libreprimus::project_name() << '\n';
    std::cout << libreprimus::version() << '\n';
    std::cout << libreprimus::stage() << '\n';
    std::cout << "CUDA enabled at build: "
              << (libreprimus::cuda_enabled_at_build() ? "true" : "false") << '\n';
    std::cout << "Stage 0A bootstrap smoke OK" << '\n';
    return 0;
}
