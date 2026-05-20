#include "libreprimus/native_cpu/native_batch.hpp"
#include "libreprimus/native_cpu/threading.hpp"

#include <iostream>
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
    const auto run = libreprimus::native_cpu::run_stage5d_fixture(1);
    failures += expect(run.backend_id == "stage5d-native-cpu-backend-v0", "backend id");
    failures += expect(run.fixture_id == "stage5d-native-synthetic-shift-fixture-v0", "fixture id");
    failures += expect(run.candidate_count == 6, "candidate count");
    failures += expect(run.result_count == run.candidate_count, "result count");
    failures += expect(run.native_cpu_only, "native CPU only");
    failures += expect(!run.cuda_used, "CUDA not used");
    failures += expect(!run.gpu_benchmark_performed, "GPU benchmark not performed");
    failures += expect(!run.solve_claim, "solve claim false");
    failures += expect(run.deterministic_ordering, "deterministic ordering");
    failures += expect(run.records.front().candidate_id == "native-shift-00", "first candidate stable");
    failures += expect(run.records.back().candidate_id == "native-shift-28", "last candidate stable");
    failures += expect(!run.output_hash.empty(), "output hash present");
    failures += expect(!run.record_hash.empty(), "record hash present");

    const auto ranges = libreprimus::native_cpu::partition_ranges(6, 4);
    failures += expect(ranges.size() == 4, "range count");
    failures += expect(ranges.front().begin == 0, "first range begins at zero");
    failures += expect(ranges.back().end == 6, "last range ends at item count");
    return failures == 0 ? 0 : 1;
}
