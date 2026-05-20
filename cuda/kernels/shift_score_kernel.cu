#include "libreprimus/shift_score_kernel.cuh"

#include <cuda_runtime.h>

namespace {

static const int kCandidateCount = libreprimus::kShiftScoreSyntheticCandidateCount;
static const int kFixtureLength = libreprimus::kShiftScoreSyntheticFixtureLength;
static const int kAlphabetSize = 26;
static const unsigned long long kFnvPrime = 1099511628211ULL;
static const char kKernelId[] = "shift_score_kernel";
static const char kBackendId[] = "stage5d-native-cpu-backend-v0";
static const char kFixtureId[] = "stage5d-native-synthetic-shift-fixture-v0";
static const char kExpectedOutputHash[] =
    "76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66";
static const int kHostShifts[kCandidateCount] = {0, 1, 3, 7, 13, 28};
static const char kCandidateIds[kCandidateCount][libreprimus::kShiftScoreSyntheticCandidateIdCapacity] = {
    "native-shift-00",
    "native-shift-01",
    "native-shift-03",
    "native-shift-07",
    "native-shift-13",
    "native-shift-28",
};

__constant__ char kDeviceFixture[kFixtureLength + 1] = "LIBER PRIMUS STAGE FIVE D";
__constant__ int kDeviceShifts[kCandidateCount] = {0, 1, 3, 7, 13, 28};

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

void append_char(char* buffer, int capacity, int* length, char value) {
    if (*length + 1 < capacity) {
        buffer[*length] = value;
        *length += 1;
        buffer[*length] = '\0';
    }
}

void append_c_string(char* buffer, int capacity, int* length, const char* value) {
    int index = 0;
    while (value[index] != '\0') {
        append_char(buffer, capacity, length, value[index]);
        ++index;
    }
}

void append_int_decimal(char* buffer, int capacity, int* length, int value) {
    if (value == 0) {
        append_char(buffer, capacity, length, '0');
        return;
    }
    if (value < 0) {
        append_char(buffer, capacity, length, '-');
        value = -value;
    }

    char digits[16];
    int digit_count = 0;
    while (value > 0 && digit_count < 16) {
        digits[digit_count] = static_cast<char>('0' + (value % 10));
        value /= 10;
        ++digit_count;
    }
    for (int index = digit_count - 1; index >= 0; --index) {
        append_char(buffer, capacity, length, digits[index]);
    }
}

unsigned long long fnv1a(const char* value, int length, unsigned long long seed) {
    unsigned long long hash = seed;
    for (int index = 0; index < length; ++index) {
        hash ^= static_cast<unsigned long long>(static_cast<unsigned char>(value[index]));
        hash *= kFnvPrime;
    }
    return hash;
}

void stable_hash_hex(const char* value, int length, char* output) {
    static const unsigned long long kSeeds[4] = {
        14695981039346656037ULL,
        1099511628211ULL,
        7809847782465536322ULL,
        1609587929392839161ULL,
    };
    static const char kHex[] = "0123456789abcdef";
    int output_index = 0;
    for (int seed_index = 0; seed_index < 4; ++seed_index) {
        const unsigned long long hash = fnv1a(value, length, kSeeds[seed_index]);
        for (int nibble = 15; nibble >= 0; --nibble) {
            output[output_index] = kHex[(hash >> (nibble * 4)) & 0xFULL];
            ++output_index;
        }
    }
    output[output_index] = '\0';
}

void build_record_material(const libreprimus::ShiftScoreSyntheticRawRecord* record, char* material, int capacity, int* length) {
    *length = 0;
    material[0] = '\0';
    append_int_decimal(material, capacity, length, record->candidate_index);
    append_char(material, capacity, length, '|');
    append_c_string(material, capacity, length, record->candidate_id);
    append_char(material, capacity, length, '|');
    append_int_decimal(material, capacity, length, record->shift);
    append_char(material, capacity, length, '|');
    append_c_string(material, capacity, length, record->output_text);
    append_char(material, capacity, length, '|');
    append_c_string(material, capacity, length, record->output_hash);
}

void build_batch_material(const libreprimus::ShiftScoreSyntheticRawRun* run, char* material, int capacity, int* length) {
    *length = 0;
    material[0] = '\0';
    append_c_string(material, capacity, length, kBackendId);
    append_char(material, capacity, length, '|');
    append_c_string(material, capacity, length, run->fixture_id);
    append_char(material, capacity, length, '|');
    for (int index = 0; index < kCandidateCount; ++index) {
        append_c_string(material, capacity, length, run->records[index].record_hash);
        append_char(material, capacity, length, '|');
    }
}

int cuda_status_code(cudaError_t status) {
    if (status == cudaSuccess) {
        return 0;
    }
    return static_cast<int>(status);
}

}  // namespace

namespace libreprimus {

int run_shift_score_synthetic_fixture_raw(ShiftScoreSyntheticRawRun* output) {
    if (output == 0) {
        return 1;
    }

    char* device_output = 0;
    const int output_size = kCandidateCount * kFixtureLength;
    cudaError_t status = cudaMalloc(&device_output, static_cast<unsigned long long>(output_size));
    if (status != cudaSuccess) {
        return cuda_status_code(status);
    }

    shift_score_synthetic_kernel<<<kCandidateCount, kFixtureLength>>>(device_output);
    status = cudaGetLastError();
    if (status != cudaSuccess) {
        cudaFree(device_output);
        return cuda_status_code(status);
    }
    status = cudaDeviceSynchronize();
    if (status != cudaSuccess) {
        cudaFree(device_output);
        return cuda_status_code(status);
    }

    char host_output[kCandidateCount * kFixtureLength];
    status = cudaMemcpy(host_output, device_output, static_cast<unsigned long long>(output_size), cudaMemcpyDeviceToHost);
    cudaError_t free_status = cudaFree(device_output);
    if (status != cudaSuccess) {
        return cuda_status_code(status);
    }
    if (free_status != cudaSuccess) {
        return cuda_status_code(free_status);
    }

    write_c_string(output->kernel_id, kShiftScoreSyntheticKernelIdCapacity, kKernelId);
    write_c_string(output->fixture_id, kShiftScoreSyntheticFixtureIdCapacity, kFixtureId);
    output->candidate_count = kCandidateCount;
    output->result_count = kCandidateCount;

    for (int index = 0; index < kCandidateCount; ++index) {
        ShiftScoreSyntheticRawRecord* record = &output->records[index];
        record->candidate_index = index;
        write_c_string(record->candidate_id, kShiftScoreSyntheticCandidateIdCapacity, kCandidateIds[index]);
        record->shift = kHostShifts[index];
        for (int text_index = 0; text_index < kFixtureLength; ++text_index) {
            record->output_text[text_index] = host_output[index * kFixtureLength + text_index];
        }
        record->output_text[kFixtureLength] = '\0';
        stable_hash_hex(record->output_text, kFixtureLength, record->output_hash);

        char record_material[256];
        int record_material_length = 0;
        build_record_material(record, record_material, 256, &record_material_length);
        stable_hash_hex(record_material, record_material_length, record->record_hash);
    }

    char batch_material[768];
    int batch_material_length = 0;
    build_batch_material(output, batch_material, 768, &batch_material_length);
    stable_hash_hex(batch_material, batch_material_length, output->output_hash);
    return 0;
}

const char* shift_score_synthetic_expected_output_hash() {
    return kExpectedOutputHash;
}

}  // namespace libreprimus
