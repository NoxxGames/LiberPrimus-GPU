#include "libreprimus/prime_minus_one_stream_kernel.cuh"

#include <cstring>
#include <iostream>

int main()
{
    libreprimus::PrimeMinusOneSyntheticRunRecord record = {};
    const int status = libreprimus::run_prime_minus_one_stream_synthetic_fixture_raw(&record);
    if (status != 0) {
        std::cerr << "prime-minus-one synthetic CUDA status=" << status << "\n";
        return status;
    }

    const int expected_values[libreprimus::kPrimeMinusOneSyntheticTokenCount] = {28, 0, -1, 27};
    const unsigned char expected_kinds[libreprimus::kPrimeMinusOneSyntheticTokenCount] = {1U, 1U, 2U, 1U};
    for (int index = 0; index < libreprimus::kPrimeMinusOneSyntheticTokenCount; ++index) {
        if (record.output_token_values[index] != expected_values[index]) {
            std::cerr << "output token mismatch at " << index << "\n";
            return 2;
        }
        if (record.output_token_kinds[index] != expected_kinds[index]) {
            std::cerr << "output token kind mismatch at " << index << "\n";
            return 3;
        }
    }

    const char* expected_hash = libreprimus::prime_minus_one_stream_synthetic_expected_output_hash();
    if (std::strcmp(record.expected_output_token_hash, expected_hash) != 0) {
        std::cerr << "expected hash mismatch\n";
        return 4;
    }
    if (std::strcmp(record.computed_output_token_hash, expected_hash) != 0) {
        std::cerr << "computed hash mismatch\n";
        return 5;
    }
    if (record.hash_match != 1) {
        std::cerr << "hash match flag mismatch\n";
        return 6;
    }
    if (record.status_codes[0] != 0) {
        std::cerr << "kernel status code mismatch\n";
        return 7;
    }

    std::cout << "validation_vector_id=" << record.validation_vector_id << "\n";
    std::cout << "mapping_id=" << record.mapping_id << "\n";
    std::cout << "computed_output_token_hash=" << record.computed_output_token_hash << "\n";
    return 0;
}
