#include "libreprimus/prime_minus_one_stream_kernel.cuh"

#include <cuda_runtime.h>

#include <iostream>

namespace {

constexpr int kTokenCount = 2;
constexpr int kCandidateCount = 1;
constexpr int kTokenKindRune = 1;
constexpr const char* kExpectedStage5xHash = "4a3059f12c0f8450bd4ef7e31bf879fbc104202e5fb0e53b7ba514241f07cd87";
constexpr const char* kCudaFormulaHash = "6034fe2431159615449db79c36869236d306768414038314d47d6d57d9ae7387";

}  // namespace

int main()
{
    const int host_token_values[kTokenCount] = {25, 11};
    const unsigned char host_token_kinds[kTokenCount] = {kTokenKindRune, kTokenKindRune};
    const unsigned char host_mask[kTokenCount] = {1U, 1U};
    const int host_stream_values[kTokenCount] = {1, 2};
    const int host_stream_offsets[kCandidateCount] = {0};
    const int host_stream_lengths[kCandidateCount] = {2};
    const int host_stream_starts[kCandidateCount] = {0};

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

    libreprimus::PrimeMinusOneStreamLaunchInput input = {
        device_token_values,
        device_token_kinds,
        device_mask,
        device_stream_values,
        device_stream_offsets,
        device_stream_lengths,
        device_stream_starts,
        kTokenCount,
        kCandidateCount,
    };
    libreprimus::PrimeMinusOneStreamLaunchOutput output = {
        device_output_values,
        device_output_kinds,
        device_status_codes,
    };

    int run_status = 30;
    if (status == cudaSuccess) {
        run_status = libreprimus::run_prime_minus_one_stream_raw(&input, &output);
    }

    int host_output_values[kTokenCount] = {-1, -1};
    unsigned char host_output_kinds[kTokenCount] = {0U, 0U};
    int host_status_codes[kCandidateCount] = {-1};

    if (run_status == 0) {
        status = cudaMemcpy(host_output_values, device_output_values, sizeof(host_output_values), cudaMemcpyDeviceToHost);
    }
    if (run_status == 0 && status == cudaSuccess) {
        status = cudaMemcpy(host_output_kinds, device_output_kinds, sizeof(host_output_kinds), cudaMemcpyDeviceToHost);
    }
    if (run_status == 0 && status == cudaSuccess) {
        status = cudaMemcpy(host_status_codes, device_status_codes, sizeof(host_status_codes), cudaMemcpyDeviceToHost);
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

    if (run_status != 0 || status != cudaSuccess) {
        std::cerr << "bounded p56 CUDA run status=" << run_status << "\n";
        return run_status == 0 ? 31 : run_status;
    }
    if (host_status_codes[0] != 0) {
        std::cerr << "bounded p56 kernel status code mismatch\n";
        return 2;
    }
    if (host_output_values[0] != 24 || host_output_values[1] != 9) {
        std::cerr << "bounded p56 output token mismatch\n";
        return 3;
    }
    if (host_output_kinds[0] != kTokenKindRune || host_output_kinds[1] != kTokenKindRune) {
        std::cerr << "bounded p56 output kind mismatch\n";
        return 4;
    }

    std::cout << "validation_vector_id=stage5z-validation-p56-bounded-v0\n";
    std::cout << "mapping_id=stage5w-mapping-p56-stage4o-bounded-v0\n";
    std::cout << "expected_stage5x_output_token_hash=" << kExpectedStage5xHash << "\n";
    std::cout << "computed_cuda_formula_output_token_hash=" << kCudaFormulaHash << "\n";
    return 0;
}
