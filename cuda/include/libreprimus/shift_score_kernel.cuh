#pragma once

namespace libreprimus {

enum {
    kShiftScoreSyntheticFixtureLength = 25,
    kShiftScoreSyntheticCandidateCount = 6,
    kShiftScoreSyntheticCandidateIdCapacity = 32,
    kShiftScoreSyntheticKernelIdCapacity = 32,
    kShiftScoreSyntheticFixtureIdCapacity = 64,
    kShiftScoreSyntheticHashCapacity = 65
};

struct ShiftScoreSyntheticRawRecord {
    int candidate_index;
    char candidate_id[kShiftScoreSyntheticCandidateIdCapacity];
    int shift;
    char output_text[kShiftScoreSyntheticFixtureLength + 1];
    char output_hash[kShiftScoreSyntheticHashCapacity];
    char record_hash[kShiftScoreSyntheticHashCapacity];
};

struct ShiftScoreSyntheticRawRun {
    char kernel_id[kShiftScoreSyntheticKernelIdCapacity];
    char fixture_id[kShiftScoreSyntheticFixtureIdCapacity];
    int candidate_count;
    int result_count;
    char output_hash[kShiftScoreSyntheticHashCapacity];
    ShiftScoreSyntheticRawRecord records[kShiftScoreSyntheticCandidateCount];
};

int run_shift_score_synthetic_fixture_raw(ShiftScoreSyntheticRawRun* output);

const char* shift_score_synthetic_expected_output_hash();

}  // namespace libreprimus
