#pragma once

#include <string>
#include <vector>

namespace libreprimus {

struct ShiftScoreSyntheticRecord {
    int candidate_index;
    std::string candidate_id;
    int shift;
    std::string output_text;
    std::string output_hash;
    std::string record_hash;
};

struct ShiftScoreSyntheticRun {
    std::string kernel_id;
    std::string fixture_id;
    int candidate_count;
    int result_count;
    std::string output_hash;
    std::vector<ShiftScoreSyntheticRecord> records;
};

ShiftScoreSyntheticRun run_shift_score_synthetic_fixture();

std::string shift_score_synthetic_output_hash();

}  // namespace libreprimus
