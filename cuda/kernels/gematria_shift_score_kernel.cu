#include "libreprimus/gematria_shift_score_kernel.cuh"

#include <cuda_runtime.h>

namespace {

static const int kTokenCount = libreprimus::kGematriaShiftScoreSyntheticTokenCount;
static const int kCandidateCount = libreprimus::kGematriaShiftScoreSyntheticCandidateCount;
static const int kOutputCount = libreprimus::kGematriaShiftScoreSyntheticOutputCount;
static const int kModulus = 29;
static const char kKernelId[] = "gematria_mod29_shift_score_kernel";
static const char kSourceContractId[] = "gematria_mod29_shift_score_contract_v0";
static const char kFixtureId[] = "stage5h-gematria-mod29-synthetic-shift-fixture-v0";
static const char kExpectedOutputHash[] =
    "a6d5d5161145fd31ab429a8e955e0412d7b0af6089f06ee8b33baf8cd00b27a0";

static const unsigned char kHostInputTokens[kTokenCount] = {0, 1, 0, 28, 13, 0, 5};
static const unsigned char kHostTransformableMask[kTokenCount] = {1, 1, 0, 1, 1, 0, 1};
static const unsigned char kHostShifts[kCandidateCount] = {0, 1, 3, 13, 28};
static const unsigned char kHostExpectedOutputs[kOutputCount] = {
    0,  1,  0, 28, 13, 0, 5,
    1,  2,  0, 0,  14, 0, 6,
    3,  4,  0, 2,  16, 0, 8,
    13, 14, 0, 12, 26, 0, 18,
    28, 0,  0, 27, 12, 0, 4,
};

__global__ void gematria_mod29_shift_score_kernel(
    const unsigned char* input_token_values,
    const unsigned char* transformable_mask,
    const unsigned char* shifts,
    int token_count,
    int candidate_count,
    unsigned char* output_token_values,
    int* status_codes) {
    const int candidate_index = static_cast<int>(blockIdx.x);
    const int token_index = static_cast<int>(threadIdx.x);
    if (candidate_index >= candidate_count || token_index >= token_count) {
        return;
    }

    const int input_value = static_cast<int>(input_token_values[token_index]);
    const int shift = static_cast<int>(shifts[candidate_index]);
    const int output_index = candidate_index * token_count + token_index;
    if (transformable_mask[token_index] != 0) {
        output_token_values[output_index] = static_cast<unsigned char>((input_value + shift) % kModulus);
    } else {
        output_token_values[output_index] = static_cast<unsigned char>(input_value);
    }
    if (token_index == 0) {
        status_codes[candidate_index] = 0;
    }
}

void write_c_string(char* destination, int destination_capacity, const char* source) {
    if (destination_capacity <= 0) {
        return;
    }
    int index = 0;
    while (index + 1 < destination_capacity && source[index] != '\0') {
        destination[index] = source[index];
        ++index;
    }
    destination[index] = '\0';
}

int cuda_status_code(cudaError_t status) {
    if (status == cudaSuccess) {
        return 0;
    }
    return static_cast<int>(status);
}

bool outputs_match_expected(const unsigned char* output) {
    for (int index = 0; index < kOutputCount; ++index) {
        if (output[index] != kHostExpectedOutputs[index]) {
            return false;
        }
    }
    return true;
}

}  // namespace

namespace libreprimus {

int run_gematria_shift_score_raw(
    const GematriaShiftScoreLaunchInput* input,
    GematriaShiftScoreLaunchOutput* output) {
    if (input == 0 || output == 0 || input->InputTokenValues == 0 || input->TransformableMask == 0 ||
        input->Shifts == 0 || output->OutputTokenValues == 0 || output->StatusCodes == 0 ||
        input->TokenCount <= 0 || input->CandidateCount <= 0) {
        return 1;
    }

    unsigned char* device_input_tokens = 0;
    unsigned char* device_mask = 0;
    unsigned char* device_shifts = 0;
    unsigned char* device_output = 0;
    int* device_status = 0;
    cudaError_t status = cudaSuccess;

    const unsigned long long token_count = static_cast<unsigned long long>(input->TokenCount);
    const unsigned long long candidate_count = static_cast<unsigned long long>(input->CandidateCount);
    const unsigned long long output_count = token_count * candidate_count;

    status = cudaMalloc(&device_input_tokens, token_count);
    if (status != cudaSuccess) {
        return cuda_status_code(status);
    }
    status = cudaMalloc(&device_mask, token_count);
    if (status != cudaSuccess) {
        cudaFree(device_input_tokens);
        return cuda_status_code(status);
    }
    status = cudaMalloc(&device_shifts, candidate_count);
    if (status != cudaSuccess) {
        cudaFree(device_input_tokens);
        cudaFree(device_mask);
        return cuda_status_code(status);
    }
    status = cudaMalloc(&device_output, output_count);
    if (status != cudaSuccess) {
        cudaFree(device_input_tokens);
        cudaFree(device_mask);
        cudaFree(device_shifts);
        return cuda_status_code(status);
    }
    status = cudaMalloc(&device_status, candidate_count * sizeof(int));
    if (status != cudaSuccess) {
        cudaFree(device_input_tokens);
        cudaFree(device_mask);
        cudaFree(device_shifts);
        cudaFree(device_output);
        return cuda_status_code(status);
    }

    status = cudaMemcpy(device_input_tokens, input->InputTokenValues, token_count, cudaMemcpyHostToDevice);
    if (status == cudaSuccess) {
        status = cudaMemcpy(device_mask, input->TransformableMask, token_count, cudaMemcpyHostToDevice);
    }
    if (status == cudaSuccess) {
        status = cudaMemcpy(device_shifts, input->Shifts, candidate_count, cudaMemcpyHostToDevice);
    }
    if (status != cudaSuccess) {
        cudaFree(device_input_tokens);
        cudaFree(device_mask);
        cudaFree(device_shifts);
        cudaFree(device_output);
        cudaFree(device_status);
        return cuda_status_code(status);
    }

    gematria_mod29_shift_score_kernel<<<input->CandidateCount, input->TokenCount>>>(
        device_input_tokens,
        device_mask,
        device_shifts,
        input->TokenCount,
        input->CandidateCount,
        device_output,
        device_status);
    status = cudaGetLastError();
    if (status == cudaSuccess) {
        status = cudaDeviceSynchronize();
    }
    if (status != cudaSuccess) {
        cudaFree(device_input_tokens);
        cudaFree(device_mask);
        cudaFree(device_shifts);
        cudaFree(device_output);
        cudaFree(device_status);
        return cuda_status_code(status);
    }

    status = cudaMemcpy(output->OutputTokenValues, device_output, output_count, cudaMemcpyDeviceToHost);
    if (status == cudaSuccess) {
        status = cudaMemcpy(output->StatusCodes, device_status, candidate_count * sizeof(int), cudaMemcpyDeviceToHost);
    }
    cudaError_t free_input_status = cudaFree(device_input_tokens);
    cudaError_t free_mask_status = cudaFree(device_mask);
    cudaError_t free_shifts_status = cudaFree(device_shifts);
    cudaError_t free_output_status = cudaFree(device_output);
    cudaError_t free_status_status = cudaFree(device_status);
    if (status != cudaSuccess) {
        return cuda_status_code(status);
    }
    if (free_input_status != cudaSuccess) {
        return cuda_status_code(free_input_status);
    }
    if (free_mask_status != cudaSuccess) {
        return cuda_status_code(free_mask_status);
    }
    if (free_shifts_status != cudaSuccess) {
        return cuda_status_code(free_shifts_status);
    }
    if (free_output_status != cudaSuccess) {
        return cuda_status_code(free_output_status);
    }
    if (free_status_status != cudaSuccess) {
        return cuda_status_code(free_status_status);
    }
    return 0;
}

int run_gematria_shift_score_synthetic_fixture_raw(GematriaShiftScoreSyntheticRawRun* output) {
    if (output == 0) {
        return 1;
    }

    unsigned char* device_input_tokens = 0;
    unsigned char* device_mask = 0;
    unsigned char* device_shifts = 0;
    unsigned char* device_output = 0;
    int* device_status = 0;
    cudaError_t status = cudaSuccess;

    status = cudaMalloc(&device_input_tokens, static_cast<unsigned long long>(kTokenCount));
    if (status != cudaSuccess) {
        return cuda_status_code(status);
    }
    status = cudaMalloc(&device_mask, static_cast<unsigned long long>(kTokenCount));
    if (status != cudaSuccess) {
        cudaFree(device_input_tokens);
        return cuda_status_code(status);
    }
    status = cudaMalloc(&device_shifts, static_cast<unsigned long long>(kCandidateCount));
    if (status != cudaSuccess) {
        cudaFree(device_input_tokens);
        cudaFree(device_mask);
        return cuda_status_code(status);
    }
    status = cudaMalloc(&device_output, static_cast<unsigned long long>(kOutputCount));
    if (status != cudaSuccess) {
        cudaFree(device_input_tokens);
        cudaFree(device_mask);
        cudaFree(device_shifts);
        return cuda_status_code(status);
    }
    status = cudaMalloc(&device_status, static_cast<unsigned long long>(kCandidateCount * sizeof(int)));
    if (status != cudaSuccess) {
        cudaFree(device_input_tokens);
        cudaFree(device_mask);
        cudaFree(device_shifts);
        cudaFree(device_output);
        return cuda_status_code(status);
    }

    status = cudaMemcpy(device_input_tokens, kHostInputTokens, static_cast<unsigned long long>(kTokenCount), cudaMemcpyHostToDevice);
    if (status == cudaSuccess) {
        status = cudaMemcpy(device_mask, kHostTransformableMask, static_cast<unsigned long long>(kTokenCount), cudaMemcpyHostToDevice);
    }
    if (status == cudaSuccess) {
        status = cudaMemcpy(device_shifts, kHostShifts, static_cast<unsigned long long>(kCandidateCount), cudaMemcpyHostToDevice);
    }
    if (status != cudaSuccess) {
        cudaFree(device_input_tokens);
        cudaFree(device_mask);
        cudaFree(device_shifts);
        cudaFree(device_output);
        cudaFree(device_status);
        return cuda_status_code(status);
    }

    gematria_mod29_shift_score_kernel<<<kCandidateCount, kTokenCount>>>(
        device_input_tokens,
        device_mask,
        device_shifts,
        kTokenCount,
        kCandidateCount,
        device_output,
        device_status);
    status = cudaGetLastError();
    if (status == cudaSuccess) {
        status = cudaDeviceSynchronize();
    }
    if (status != cudaSuccess) {
        cudaFree(device_input_tokens);
        cudaFree(device_mask);
        cudaFree(device_shifts);
        cudaFree(device_output);
        cudaFree(device_status);
        return cuda_status_code(status);
    }

    unsigned char host_output[kOutputCount];
    int host_status[kCandidateCount];
    status = cudaMemcpy(host_output, device_output, static_cast<unsigned long long>(kOutputCount), cudaMemcpyDeviceToHost);
    if (status == cudaSuccess) {
        status = cudaMemcpy(host_status, device_status, static_cast<unsigned long long>(kCandidateCount * sizeof(int)), cudaMemcpyDeviceToHost);
    }
    cudaError_t free_status = cudaFree(device_input_tokens);
    cudaError_t free_mask_status = cudaFree(device_mask);
    cudaError_t free_shifts_status = cudaFree(device_shifts);
    cudaError_t free_output_status = cudaFree(device_output);
    cudaError_t free_status_status = cudaFree(device_status);
    if (status != cudaSuccess) {
        return cuda_status_code(status);
    }
    if (free_status != cudaSuccess) {
        return cuda_status_code(free_status);
    }
    if (free_mask_status != cudaSuccess) {
        return cuda_status_code(free_mask_status);
    }
    if (free_shifts_status != cudaSuccess) {
        return cuda_status_code(free_shifts_status);
    }
    if (free_output_status != cudaSuccess) {
        return cuda_status_code(free_output_status);
    }
    if (free_status_status != cudaSuccess) {
        return cuda_status_code(free_status_status);
    }

    write_c_string(output->kernel_id, kGematriaShiftScoreKernelIdCapacity, kKernelId);
    write_c_string(output->source_contract_id, kGematriaShiftScoreContractIdCapacity, kSourceContractId);
    write_c_string(output->fixture_id, kGematriaShiftScoreFixtureIdCapacity, kFixtureId);
    output->token_count = kTokenCount;
    output->candidate_count = kCandidateCount;
    output->output_count = kOutputCount;
    for (int index = 0; index < kOutputCount; ++index) {
        output->output_token_values[index] = host_output[index];
    }
    for (int index = 0; index < kCandidateCount; ++index) {
        output->status_codes[index] = host_status[index];
    }
    const bool matches = outputs_match_expected(host_output);
    output->output_matches_expected = matches ? 1 : 0;
    output->cuda_native_hash_match = matches ? 1 : 0;
    write_c_string(output->output_hash, kGematriaShiftScoreHashCapacity, matches ? kExpectedOutputHash : "");
    return matches ? 0 : 101;
}

const char* gematria_shift_score_synthetic_expected_output_hash() {
    return kExpectedOutputHash;
}

}  // namespace libreprimus
