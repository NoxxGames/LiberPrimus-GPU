#include "libreprimus/shift_score_kernel.cuh"

#include <exception>
#include <iostream>
#include <string>

int main() {
    try {
        const std::string expected = "76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66";
        const auto run = libreprimus::run_shift_score_synthetic_fixture();
        if (run.kernel_id != "shift_score_kernel") {
            std::cerr << "Unexpected kernel id: " << run.kernel_id << '\n';
            return 1;
        }
        if (run.candidate_count != 6 || run.result_count != 6) {
            std::cerr << "Unexpected synthetic candidate/result count\n";
            return 1;
        }
        if (run.output_hash != expected) {
            std::cerr << "Unexpected shift_score synthetic hash: " << run.output_hash << '\n';
            return 1;
        }
    } catch (const std::exception& error) {
        std::cerr << "CUDA shift_score synthetic parity failed: " << error.what() << '\n';
        return 1;
    }

    return 0;
}
