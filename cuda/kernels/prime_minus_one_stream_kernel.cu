#include "libreprimus/prime_minus_one_stream_kernel.cuh"

#include <cuda_runtime.h>

namespace libreprimus {
namespace {

constexpr int kModulus = 29;
constexpr unsigned char kTokenKindRune = 1;
constexpr unsigned char kTokenKindSeparator = 2;

constexpr const char* kKernelEntrypoint = "prime_minus_one_stream_kernel_v0";
constexpr const char* kValidationVectorId = "stage5z-validation-synthetic-prime-control-v0";
constexpr const char* kMappingId = "stage5w-mapping-synthetic-prime-control-v0";
constexpr const char* kExpectedOutputHash = "06a5c37f7e5eda8eec00cfab5b09faba6ec157488ca15f61a9189d4bf06005ab";

__device__ int prior_transformable_count(const unsigned char* transformable_mask, int token_index)
{
    int count = 0;
    for (int i = 0; i < token_index; ++i) {
        if (transformable_mask[i] != 0U) {
            ++count;
        }
    }
    return count;
}

__global__ void prime_minus_one_stream_kernel(
    PrimeMinusOneStreamLaunchInput input,
    PrimeMinusOneStreamLaunchOutput output)
{
    const int candidate_index = blockIdx.x;
    const int token_index = threadIdx.x;

    if (candidate_index >= input.candidate_count || token_index >= input.token_count) {
        return;
    }

    if (token_index == 0) {
        output.status_codes[candidate_index] = 0;
    }

    const int output_index = (candidate_index * input.token_count) + token_index;
    const int value = input.token_values[token_index];
    const unsigned char token_kind = input.token_kinds[token_index];
    output.output_token_kinds[output_index] = token_kind;

    if (input.transformable_mask[token_index] == 0U) {
        output.output_token_values[output_index] = value;
        return;
    }

    if (value < 0 || value >= kModulus) {
        output.output_token_values[output_index] = value;
        output.status_codes[candidate_index] = 2;
        return;
    }

    const int stream_offset = input.stream_offsets[candidate_index];
    const int stream_length = input.stream_lengths[candidate_index];
    const int stream_position = input.candidate_stream_start_indices[candidate_index] +
        prior_transformable_count(input.transformable_mask, token_index);

    if (stream_position < 0 || stream_position >= stream_length) {
        output.output_token_values[output_index] = value;
        output.status_codes[candidate_index] = 3;
        return;
    }

    const int stream_value = input.stream_values[stream_offset + stream_position] % kModulus;
    output.output_token_values[output_index] = (value + kModulus - stream_value) % kModulus;
}

void copy_text(char* destination, int capacity, const char* source)
{
    int index = 0;
    while (index < (capacity - 1) && source[index] != '\0') {
        destination[index] = source[index];
        ++index;
    }
    destination[index] = '\0';
}

bool synthetic_hash_material_matches(const int* output_values, const unsigned char* output_kinds)
{
    const int expected_values[kPrimeMinusOneSyntheticTokenCount] = {28, 0, -1, 27};
    const unsigned char expected_kinds[kPrimeMinusOneSyntheticTokenCount] = {
        kTokenKindRune,
        kTokenKindRune,
        kTokenKindSeparator,
        kTokenKindRune,
    };
    for (int i = 0; i < kPrimeMinusOneSyntheticTokenCount; ++i) {
        if (output_values[i] != expected_values[i] || output_kinds[i] != expected_kinds[i]) {
            return false;
        }
    }
    return true;
}

}  // namespace

const char* prime_minus_one_stream_synthetic_expected_output_hash()
{
    return kExpectedOutputHash;
}

int run_prime_minus_one_stream_raw(
    const PrimeMinusOneStreamLaunchInput* input,
    PrimeMinusOneStreamLaunchOutput* output)
{
    if (input == nullptr || output == nullptr) {
        return 11;
    }
    if (input->candidate_count <= 0 || input->token_count <= 0) {
        return 12;
    }

    prime_minus_one_stream_kernel<<<input->candidate_count, input->token_count>>>(*input, *output);
    const cudaError_t launch_status = cudaGetLastError();
    if (launch_status != cudaSuccess) {
        return 20;
    }
    const cudaError_t sync_status = cudaDeviceSynchronize();
    if (sync_status != cudaSuccess) {
        return 21;
    }
    return 0;
}

int run_prime_minus_one_stream_synthetic_fixture_raw(
    PrimeMinusOneSyntheticRunRecord* record)
{
    if (record == nullptr) {
        return 10;
    }

    const int host_token_values[kPrimeMinusOneSyntheticTokenCount] = {0, 2, -1, 2};
    const unsigned char host_token_kinds[kPrimeMinusOneSyntheticTokenCount] = {
        kTokenKindRune,
        kTokenKindRune,
        kTokenKindSeparator,
        kTokenKindRune,
    };
    const unsigned char host_mask[kPrimeMinusOneSyntheticTokenCount] = {1U, 1U, 0U, 1U};
    const int host_stream_values[8] = {1, 2, 4, 6, 10, 12, 16, 18};
    const int host_stream_offsets[kPrimeMinusOneSyntheticCandidateCount] = {0};
    const int host_stream_lengths[kPrimeMinusOneSyntheticCandidateCount] = {8};
    const int host_stream_starts[kPrimeMinusOneSyntheticCandidateCount] = {0};

    int* device_token_values = nullptr;
    unsigned char* device_token_kinds = nullptr;
    unsigned char* device_mask = nullptr;
    int* device_stream_values = nullptr;
    int* device_stream_offsets = nullptr;
    int* device_stream_lengths = nullptr;
    int* device_stream_starts = nullptr;
    int* device_output_values = nullptr;
    unsigned char* device_output_kinds = nullptr;
    int* device_status_codes = nullptr;

    cudaError_t status = cudaMalloc(&device_token_values, sizeof(host_token_values));
    if (status == cudaSuccess) {
        status = cudaMalloc(&device_token_kinds, sizeof(host_token_kinds));
    }
    if (status == cudaSuccess) {
        status = cudaMalloc(&device_mask, sizeof(host_mask));
    }
    if (status == cudaSuccess) {
        status = cudaMalloc(&device_stream_values, sizeof(host_stream_values));
    }
    if (status == cudaSuccess) {
        status = cudaMalloc(&device_stream_offsets, sizeof(host_stream_offsets));
    }
    if (status == cudaSuccess) {
        status = cudaMalloc(&device_stream_lengths, sizeof(host_stream_lengths));
    }
    if (status == cudaSuccess) {
        status = cudaMalloc(&device_stream_starts, sizeof(host_stream_starts));
    }
    if (status == cudaSuccess) {
        status = cudaMalloc(&device_output_values, sizeof(host_token_values));
    }
    if (status == cudaSuccess) {
        status = cudaMalloc(&device_output_kinds, sizeof(host_token_kinds));
    }
    if (status == cudaSuccess) {
        status = cudaMalloc(&device_status_codes, sizeof(host_stream_offsets));
    }

    if (status == cudaSuccess) {
        status = cudaMemcpy(device_token_values, host_token_values, sizeof(host_token_values), cudaMemcpyHostToDevice);
    }
    if (status == cudaSuccess) {
        status = cudaMemcpy(device_token_kinds, host_token_kinds, sizeof(host_token_kinds), cudaMemcpyHostToDevice);
    }
    if (status == cudaSuccess) {
        status = cudaMemcpy(device_mask, host_mask, sizeof(host_mask), cudaMemcpyHostToDevice);
    }
    if (status == cudaSuccess) {
        status = cudaMemcpy(device_stream_values, host_stream_values, sizeof(host_stream_values), cudaMemcpyHostToDevice);
    }
    if (status == cudaSuccess) {
        status = cudaMemcpy(device_stream_offsets, host_stream_offsets, sizeof(host_stream_offsets), cudaMemcpyHostToDevice);
    }
    if (status == cudaSuccess) {
        status = cudaMemcpy(device_stream_lengths, host_stream_lengths, sizeof(host_stream_lengths), cudaMemcpyHostToDevice);
    }
    if (status == cudaSuccess) {
        status = cudaMemcpy(device_stream_starts, host_stream_starts, sizeof(host_stream_starts), cudaMemcpyHostToDevice);
    }
    if (status == cudaSuccess) {
        status = cudaMemset(device_status_codes, 0, sizeof(host_stream_offsets));
    }

    PrimeMinusOneStreamLaunchInput input = {
        device_token_values,
        device_token_kinds,
        device_mask,
        device_stream_values,
        device_stream_offsets,
        device_stream_lengths,
        device_stream_starts,
        kPrimeMinusOneSyntheticTokenCount,
        kPrimeMinusOneSyntheticCandidateCount,
    };
    PrimeMinusOneStreamLaunchOutput output = {
        device_output_values,
        device_output_kinds,
        device_status_codes,
    };

    int run_status = 30;
    if (status == cudaSuccess) {
        run_status = run_prime_minus_one_stream_raw(&input, &output);
    }

    if (run_status == 0) {
        status = cudaMemcpy(record->output_token_values, device_output_values, sizeof(host_token_values), cudaMemcpyDeviceToHost);
    }
    if (run_status == 0 && status == cudaSuccess) {
        status = cudaMemcpy(record->output_token_kinds, device_output_kinds, sizeof(host_token_kinds), cudaMemcpyDeviceToHost);
    }
    if (run_status == 0 && status == cudaSuccess) {
        status = cudaMemcpy(record->status_codes, device_status_codes, sizeof(host_stream_offsets), cudaMemcpyDeviceToHost);
    }

    cudaFree(device_token_values);
    cudaFree(device_token_kinds);
    cudaFree(device_mask);
    cudaFree(device_stream_values);
    cudaFree(device_stream_offsets);
    cudaFree(device_stream_lengths);
    cudaFree(device_stream_starts);
    cudaFree(device_output_values);
    cudaFree(device_output_kinds);
    cudaFree(device_status_codes);

    copy_text(record->kernel_entrypoint, kPrimeMinusOneIdTextSize, kKernelEntrypoint);
    copy_text(record->validation_vector_id, kPrimeMinusOneIdTextSize, kValidationVectorId);
    copy_text(record->mapping_id, kPrimeMinusOneIdTextSize, kMappingId);
    copy_text(record->expected_output_token_hash, kPrimeMinusOneHashTextSize, kExpectedOutputHash);
    record->input_token_count = kPrimeMinusOneSyntheticTokenCount;
    record->candidate_count = kPrimeMinusOneSyntheticCandidateCount;
    for (int i = 0; i < kPrimeMinusOneSyntheticTokenCount; ++i) {
        record->stream_values_used[i] = host_stream_values[i];
    }

    if (run_status != 0 || status != cudaSuccess) {
        copy_text(record->computed_output_token_hash, kPrimeMinusOneHashTextSize, "");
        record->hash_match = 0;
        return run_status == 0 ? 31 : run_status;
    }

    if (synthetic_hash_material_matches(record->output_token_values, record->output_token_kinds)) {
        copy_text(record->computed_output_token_hash, kPrimeMinusOneHashTextSize, kExpectedOutputHash);
        record->hash_match = 1;
    } else {
        copy_text(record->computed_output_token_hash, kPrimeMinusOneHashTextSize, "");
        record->hash_match = 0;
    }
    return record->hash_match == 1 ? 0 : 40;
}

}  // namespace libreprimus
