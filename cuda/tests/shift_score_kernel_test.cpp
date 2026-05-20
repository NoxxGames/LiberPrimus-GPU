#include "libreprimus/shift_score_kernel.cuh"

#include <cstring>
#include <iostream>

int main() {
    libreprimus::ShiftScoreSyntheticRawRun run{};
    const int status = libreprimus::run_shift_score_synthetic_fixture_raw(&run);
    if (status != 0) {
        std::cerr << "CUDA shift_score synthetic parity failed with status " << status << '\n';
        return 1;
    }
    if (std::strcmp(run.kernel_id, "shift_score_kernel") != 0) {
        std::cerr << "Unexpected kernel id: " << run.kernel_id << '\n';
        return 1;
    }
    if (run.candidate_count != 6 || run.result_count != 6) {
        std::cerr << "Unexpected synthetic candidate/result count\n";
        return 1;
    }
    if (std::strcmp(run.output_hash, libreprimus::shift_score_synthetic_expected_output_hash()) != 0) {
        std::cerr << "Unexpected shift_score synthetic hash: " << run.output_hash << '\n';
        return 1;
    }

    return 0;
}
