#include "libreprimus/gematria_shift_score_kernel.cuh"

#include <fstream>
#include <iostream>
#include <string>
#include <vector>

namespace {

bool read_vector(std::istream& input, std::vector<unsigned char>& output, int count) {
    for (int index = 0; index < count; ++index) {
        int value = -1;
        if (!(input >> value) || value < 0 || value > 255) {
            return false;
        }
        output.push_back(static_cast<unsigned char>(value));
    }
    return true;
}

void print_vector(const std::vector<unsigned char>& values) {
    for (std::size_t index = 0; index < values.size(); ++index) {
        if (index != 0) {
            std::cout << ',';
        }
        std::cout << static_cast<int>(values[index]);
    }
}

void print_vector(const std::vector<int>& values) {
    for (std::size_t index = 0; index < values.size(); ++index) {
        if (index != 0) {
            std::cout << ',';
        }
        std::cout << values[index];
    }
}

}  // namespace

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "usage: gematria_shift_score_stage5m_runner <input.txt>\n";
        return 2;
    }

    std::ifstream input(argv[1]);
    if (!input) {
        std::cerr << "unable to open input file\n";
        return 3;
    }

    int token_count = 0;
    int candidate_count = 0;
    if (!(input >> token_count >> candidate_count) || token_count <= 0 || candidate_count <= 0 || token_count > 1024) {
        std::cerr << "invalid token/candidate counts\n";
        return 4;
    }

    std::vector<unsigned char> input_tokens;
    std::vector<unsigned char> transformable_mask;
    std::vector<unsigned char> shifts;
    input_tokens.reserve(static_cast<std::size_t>(token_count));
    transformable_mask.reserve(static_cast<std::size_t>(token_count));
    shifts.reserve(static_cast<std::size_t>(candidate_count));

    if (!read_vector(input, input_tokens, token_count) || !read_vector(input, transformable_mask, token_count) ||
        !read_vector(input, shifts, candidate_count)) {
        std::cerr << "invalid input vector\n";
        return 5;
    }

    std::vector<unsigned char> output_tokens(static_cast<std::size_t>(token_count * candidate_count), 0);
    std::vector<int> status_codes(static_cast<std::size_t>(candidate_count), -1);
    libreprimus::GematriaShiftScoreLaunchInput launch_input{
        input_tokens.data(),
        transformable_mask.data(),
        shifts.data(),
        token_count,
        candidate_count,
    };
    libreprimus::GematriaShiftScoreLaunchOutput launch_output{
        output_tokens.data(),
        status_codes.data(),
    };

    const int status = libreprimus::run_gematria_shift_score_raw(&launch_input, &launch_output);
    std::cout << "status=" << status << '\n';
    std::cout << "output_token_values=";
    print_vector(output_tokens);
    std::cout << '\n';
    std::cout << "status_codes=";
    print_vector(status_codes);
    std::cout << '\n';
    return status == 0 ? 0 : 10;
}
