#pragma once

#include <cstddef>
#include <string>
#include <vector>

namespace libreprimus::native_cpu {

struct Candidate {
    std::string candidate_id;
    int shift;
};

struct ResultRecord {
    std::size_t candidate_index;
    std::string candidate_id;
    int shift;
    std::string output_text;
    std::string output_hash;
    std::string record_hash;
};

struct BatchRun {
    std::string backend_id;
    std::string fixture_id;
    std::size_t thread_count;
    std::size_t candidate_count;
    std::size_t result_count;
    std::string output_hash;
    std::string record_hash;
    bool deterministic_ordering;
    bool native_cpu_only;
    bool cuda_used;
    bool gpu_benchmark_performed;
    bool solve_claim;
    std::vector<ResultRecord> records;
};

std::vector<Candidate> stage5d_candidates();
std::string stage5d_fixture_text();
BatchRun run_stage5d_fixture(std::size_t requested_threads);
std::string to_json(const BatchRun& run);

}  // namespace libreprimus::native_cpu
