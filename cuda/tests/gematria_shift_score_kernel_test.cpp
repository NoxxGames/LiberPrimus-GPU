#include "libreprimus/gematria_shift_score_kernel.cuh"

#include <cstring>
#include <iostream>

int main() {
    libreprimus::GematriaShiftScoreSyntheticRawRun run{};
    const int status = libreprimus::run_gematria_shift_score_synthetic_fixture_raw(&run);
    if (status != 0) {
        std::cerr << "Gematria CUDA synthetic parity failed with status " << status << '\n';
        return 1;
    }
    if (std::strcmp(run.kernel_id, "gematria_mod29_shift_score_kernel") != 0) {
        std::cerr << "Unexpected kernel id: " << run.kernel_id << '\n';
        return 1;
    }
    if (std::strcmp(run.source_contract_id, "gematria_mod29_shift_score_contract_v0") != 0) {
        std::cerr << "Unexpected contract id: " << run.source_contract_id << '\n';
        return 1;
    }
    if (std::strcmp(run.fixture_id, "stage5h-gematria-mod29-synthetic-shift-fixture-v0") != 0) {
        std::cerr << "Unexpected fixture id: " << run.fixture_id << '\n';
        return 1;
    }
    if (run.token_count != 7 || run.candidate_count != 5 || run.output_count != 35) {
        std::cerr << "Unexpected synthetic vector shape\n";
        return 1;
    }
    const unsigned char expected[35] = {
        0,  1,  0, 28, 13, 0, 5,
        1,  2,  0, 0,  14, 0, 6,
        3,  4,  0, 2,  16, 0, 8,
        13, 14, 0, 12, 26, 0, 18,
        28, 0,  0, 27, 12, 0, 4,
    };
    for (int index = 0; index < 35; ++index) {
        if (run.output_token_values[index] != expected[index]) {
            std::cerr << "Unexpected output token at " << index << '\n';
            return 1;
        }
    }
    for (int index = 0; index < 5; ++index) {
        if (run.status_codes[index] != 0) {
            std::cerr << "Unexpected candidate status at " << index << '\n';
            return 1;
        }
    }
    if (std::strcmp(run.output_hash, libreprimus::gematria_shift_score_synthetic_expected_output_hash()) != 0) {
        std::cerr << "Unexpected Gematria synthetic hash: " << run.output_hash << '\n';
        return 1;
    }
    if (run.output_matches_expected != 1 || run.cuda_native_hash_match != 1) {
        std::cerr << "Gematria synthetic parity flags were not set\n";
        return 1;
    }
    return 0;
}
