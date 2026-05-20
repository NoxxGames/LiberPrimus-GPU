#include "libreprimus/shift_score_kernel.cuh"

#include <cuda_runtime.h>

#include <array>
#include <cstdint>
#include <iomanip>
#include <sstream>
#include <stdexcept>

namespace {

constexpr int kFixtureLength = 25;
constexpr int kCandidateCount = 6;
constexpr int kHostShifts[kCandidateCount] = {0, 1, 3, 7, 13, 28};
__constant__ char kDeviceFixture[kFixtureLength + 1] = "LIBER PRIMUS STAGE FIVE D";
__constant__ int kDeviceShifts[kCandidateCount] = {0, 1, 3, 7, 13, 28};
constexpr std::array<const char*, kCandidateCount> kCandidateIds{
    "native-shift-00",
    "native-shift-01",
    "native-shift-03",
    "native-shift-07",
    "native-shift-13",
    "native-shift-28",
};
constexpr char kKernelId[] = "shift_score_kernel";
constexpr char kBackendId[] = "stage5d-native-cpu-backend-v0";
constexpr char kFixtureId[] = "stage5d-native-synthetic-shift-fixture-v0";
constexpr int kAlphabetSize = 26;
constexpr std::uint64_t kFnvPrime = 1099511628211ULL;

__device__ char shift_synthetic_char(char value, int shift) {
    if (value >= 'a' && value <= 'z') {
        value = static_cast<char>(value - ('a' - 'A'));
    }
    if (value >= 'A' && value <= 'Z') {
        const int offset = static_cast<int>(value) - static_cast<int>('A');
        const int shifted = (offset + shift + kAlphabetSize * 4) % kAlphabetSize;
        return static_cast<char>(static_cast<int>('A') + shifted);
    }
    return value;
}

__global__ void shift_score_synthetic_kernel(char* output) {
    const int candidate = static_cast<int>(blockIdx.x);
    const int index = static_cast<int>(threadIdx.x);
    if (candidate >= kCandidateCount || index >= kFixtureLength) {
        return;
    }
    output[candidate * kFixtureLength + index] = shift_synthetic_char(kDeviceFixture[index], kDeviceShifts[candidate]);
}

void check_cuda(cudaError_t status, const char* operation) {
    if (status != cudaSuccess) {
        throw std::runtime_error(std::string(operation) + " failed: " + cudaGetErrorString(status));
    }
}

std::uint64_t fnv1a(std::string_view value, std::uint64_t seed) {
    std::uint64_t hash = seed;
    for (const unsigned char ch : value) {
        hash ^= static_cast<std::uint64_t>(ch);
        hash *= kFnvPrime;
    }
    return hash;
}

std::string stable_hash_hex(std::string_view value) {
    constexpr std::array<std::uint64_t, 4> seeds{
        14695981039346656037ULL,
        1099511628211ULL,
        7809847782465536322ULL,
        1609587929392839161ULL,
    };
    std::ostringstream out;
    out << std::hex << std::setfill('0');
    for (const auto seed : seeds) {
        out << std::setw(16) << fnv1a(value, seed);
    }
    return out.str();
}

std::string record_material(const libreprimus::ShiftScoreSyntheticRecord& record) {
    std::ostringstream out;
    out << record.candidate_index << '|'
        << record.candidate_id << '|'
        << record.shift << '|'
        << record.output_text << '|'
        << record.output_hash;
    return out.str();
}

std::string batch_material(const libreprimus::ShiftScoreSyntheticRun& run) {
    std::ostringstream out;
    out << kBackendId << '|' << run.fixture_id << '|';
    for (const auto& record : run.records) {
        out << record.record_hash << '|';
    }
    return out.str();
}

}  // namespace

namespace libreprimus {

ShiftScoreSyntheticRun run_shift_score_synthetic_fixture() {
    char* device_output = nullptr;
    constexpr std::size_t output_size = static_cast<std::size_t>(kCandidateCount * kFixtureLength);
    check_cuda(cudaMalloc(&device_output, output_size), "cudaMalloc");

    shift_score_synthetic_kernel<<<kCandidateCount, kFixtureLength>>>(device_output);
    check_cuda(cudaGetLastError(), "shift_score_synthetic_kernel launch");
    check_cuda(cudaDeviceSynchronize(), "cudaDeviceSynchronize");

    std::string host_output(output_size, '\0');
    try {
        check_cuda(cudaMemcpy(host_output.data(), device_output, output_size, cudaMemcpyDeviceToHost), "cudaMemcpy");
        check_cuda(cudaFree(device_output), "cudaFree");
    } catch (...) {
        cudaFree(device_output);
        throw;
    }

    ShiftScoreSyntheticRun run;
    run.kernel_id = kKernelId;
    run.fixture_id = kFixtureId;
    run.candidate_count = kCandidateCount;
    run.result_count = kCandidateCount;
    run.records.reserve(kCandidateCount);
    for (int index = 0; index < kCandidateCount; ++index) {
        ShiftScoreSyntheticRecord record;
        record.candidate_index = index;
        record.candidate_id = kCandidateIds[static_cast<std::size_t>(index)];
        record.shift = kHostShifts[index];
        record.output_text = host_output.substr(static_cast<std::size_t>(index * kFixtureLength), kFixtureLength);
        record.output_hash = stable_hash_hex(record.output_text);
        record.record_hash = stable_hash_hex(record_material(record));
        run.records.push_back(std::move(record));
    }
    run.output_hash = stable_hash_hex(batch_material(run));
    return run;
}

std::string shift_score_synthetic_output_hash() {
    return run_shift_score_synthetic_fixture().output_hash;
}

}  // namespace libreprimus
