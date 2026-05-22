#pragma once

namespace libreprimus {

constexpr int kPrimeMinusOneSyntheticTokenCount = 4;
constexpr int kPrimeMinusOneSyntheticCandidateCount = 1;
constexpr int kPrimeMinusOneHashTextSize = 65;
constexpr int kPrimeMinusOneIdTextSize = 96;

struct PrimeMinusOneStreamLaunchInput {
    const int* token_values;
    const unsigned char* token_kinds;
    const unsigned char* transformable_mask;
    const int* stream_values;
    const int* stream_offsets;
    const int* stream_lengths;
    const int* candidate_stream_start_indices;
    int token_count;
    int candidate_count;
};

struct PrimeMinusOneStreamLaunchOutput {
    int* output_token_values;
    unsigned char* output_token_kinds;
    int* status_codes;
};

struct PrimeMinusOneSyntheticRunRecord {
    char kernel_entrypoint[kPrimeMinusOneIdTextSize];
    char validation_vector_id[kPrimeMinusOneIdTextSize];
    char mapping_id[kPrimeMinusOneIdTextSize];
    char expected_output_token_hash[kPrimeMinusOneHashTextSize];
    char computed_output_token_hash[kPrimeMinusOneHashTextSize];
    int input_token_count;
    int candidate_count;
    int output_token_values[kPrimeMinusOneSyntheticTokenCount];
    unsigned char output_token_kinds[kPrimeMinusOneSyntheticTokenCount];
    int stream_values_used[kPrimeMinusOneSyntheticTokenCount];
    int status_codes[kPrimeMinusOneSyntheticCandidateCount];
    int hash_match;
};

const char* prime_minus_one_stream_synthetic_expected_output_hash();

int run_prime_minus_one_stream_raw(
    const PrimeMinusOneStreamLaunchInput* input,
    PrimeMinusOneStreamLaunchOutput* output);

int run_prime_minus_one_stream_synthetic_fixture_raw(
    PrimeMinusOneSyntheticRunRecord* record);

}  // namespace libreprimus
