#include "libreprimus/cuda_smoke.cuh"

#include <exception>
#include <iostream>

int main() {
    try {
        const int value = libreprimus::cuda_smoke_value();
        if (value != 20260515) {
            std::cerr << "Unexpected CUDA smoke value: " << value << '\n';
            return 1;
        }
    } catch (const std::exception& error) {
        std::cerr << "CUDA smoke failed: " << error.what() << '\n';
        return 1;
    }

    return 0;
}
