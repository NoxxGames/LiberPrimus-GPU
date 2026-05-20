#include "libreprimus/native_cpu/native_batch.hpp"

#include <array>
#include <iostream>
#include <string>
#include <string_view>

namespace {

int expect(bool condition, std::string_view message) {
    if (condition) {
        return 0;
    }
    std::cerr << "FAILED: " << message << '\n';
    return 1;
}

}  // namespace

int main() {
    int failures = 0;
    const auto one = libreprimus::native_cpu::run_stage5d_fixture(1);
    constexpr std::array<std::size_t, 5> thread_counts{1, 2, 4, 8, 16};
    for (const auto count : thread_counts) {
        const auto run = libreprimus::native_cpu::run_stage5d_fixture(count);
        failures += expect(run.output_hash == one.output_hash, "output hash stable across threads");
        failures += expect(run.records.size() == one.records.size(), "record count stable across threads");
        for (std::size_t index = 0; index < run.records.size(); ++index) {
            failures += expect(run.records[index].candidate_index == index, "candidate index stable");
            failures += expect(run.records[index].candidate_id == one.records[index].candidate_id, "candidate id stable");
            failures += expect(run.records[index].record_hash == one.records[index].record_hash, "record hash stable");
        }
    }
    return failures == 0 ? 0 : 1;
}
