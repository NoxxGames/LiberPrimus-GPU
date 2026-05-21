#pragma once

namespace libreprimus {

enum {
    kGematriaShiftScoreSyntheticTokenCount = 7,
    kGematriaShiftScoreSyntheticCandidateCount = 5,
    kGematriaShiftScoreSyntheticOutputCount = 35,
    kGematriaShiftScoreKernelIdCapacity = 48,
    kGematriaShiftScoreContractIdCapacity = 64,
    kGematriaShiftScoreFixtureIdCapacity = 72,
    kGematriaShiftScoreHashCapacity = 65
};

struct GematriaShiftScoreLaunchInput {
    const unsigned char* InputTokenValues;
    const unsigned char* TransformableMask;
    const unsigned char* Shifts;
    int TokenCount;
    int CandidateCount;
};

struct GematriaShiftScoreLaunchOutput {
    unsigned char* OutputTokenValues;
    int* StatusCodes;
};

struct GematriaShiftScoreSyntheticRawRun {
    char kernel_id[kGematriaShiftScoreKernelIdCapacity];
    char source_contract_id[kGematriaShiftScoreContractIdCapacity];
    char fixture_id[kGematriaShiftScoreFixtureIdCapacity];
    int token_count;
    int candidate_count;
    int output_count;
    unsigned char output_token_values[kGematriaShiftScoreSyntheticOutputCount];
    int status_codes[kGematriaShiftScoreSyntheticCandidateCount];
    char output_hash[kGematriaShiftScoreHashCapacity];
    int output_matches_expected;
    int cuda_native_hash_match;
};

int run_gematria_shift_score_synthetic_fixture_raw(GematriaShiftScoreSyntheticRawRun* output);

int run_gematria_shift_score_raw(
    const GematriaShiftScoreLaunchInput* input,
    GematriaShiftScoreLaunchOutput* output);

const char* gematria_shift_score_synthetic_expected_output_hash();

}  // namespace libreprimus
