#include "libreprimus/native_cpu/native_batch.hpp"

#include "libreprimus/native_cpu/hash.hpp"
#include "libreprimus/native_cpu/threading.hpp"

#include <algorithm>
#include <cctype>
#include <exception>
#include <mutex>
#include <sstream>
#include <stdexcept>
#include <thread>

namespace libreprimus::native_cpu {

namespace {

constexpr int alphabet_size = 26;

char shift_letter(char value, int shift) {
    const int base = static_cast<int>('A');
    const int offset = static_cast<int>(value) - base;
    const int shifted = (offset + shift + alphabet_size * 4) % alphabet_size;
    return static_cast<char>(base + shifted);
}

std::string apply_shift(std::string_view fixture, int shift) {
    std::string output;
    output.reserve(fixture.size());
    for (const char ch : fixture) {
        const unsigned char uch = static_cast<unsigned char>(ch);
        if (std::isalpha(uch) != 0) {
            output.push_back(shift_letter(static_cast<char>(std::toupper(uch)), shift));
        } else {
            output.push_back(ch);
        }
    }
    return output;
}

std::string record_material(const ResultRecord& record) {
    std::ostringstream out;
    out << record.candidate_index << '|'
        << record.candidate_id << '|'
        << record.shift << '|'
        << record.output_text << '|'
        << record.output_hash;
    return out.str();
}

ResultRecord build_record(std::size_t index, const Candidate& candidate, std::string_view fixture) {
    ResultRecord record;
    record.candidate_index = index;
    record.candidate_id = candidate.candidate_id;
    record.shift = candidate.shift;
    record.output_text = apply_shift(fixture, candidate.shift);
    record.output_hash = stable_hash_hex(record.output_text);
    record.record_hash = stable_hash_hex(record_material(record));
    return record;
}

std::string json_escape(std::string_view value) {
    std::string out;
    out.reserve(value.size() + 4);
    for (const char ch : value) {
        if (ch == '\\' || ch == '"') {
            out.push_back('\\');
            out.push_back(ch);
        } else if (ch == '\n') {
            out += "\\n";
        } else {
            out.push_back(ch);
        }
    }
    return out;
}

std::string batch_material(const BatchRun& run) {
    std::ostringstream out;
    out << run.backend_id << '|' << run.fixture_id << '|';
    for (const auto& record : run.records) {
        out << record.record_hash << '|';
    }
    return out.str();
}

}  // namespace

std::vector<Candidate> stage5d_candidates() {
    return {
        Candidate{"native-shift-00", 0},
        Candidate{"native-shift-01", 1},
        Candidate{"native-shift-03", 3},
        Candidate{"native-shift-07", 7},
        Candidate{"native-shift-13", 13},
        Candidate{"native-shift-28", 28},
    };
}

std::string stage5d_fixture_text() {
    return "LIBER PRIMUS STAGE FIVE D";
}

BatchRun run_stage5d_fixture(std::size_t requested_threads) {
    const auto candidates = stage5d_candidates();
    const auto fixture = stage5d_fixture_text();
    std::vector<ResultRecord> records(candidates.size());
    std::vector<std::string> worker_errors;
    std::mutex error_mutex;
    const auto ranges = partition_ranges(candidates.size(), std::max<std::size_t>(1, requested_threads));
    std::vector<std::thread> workers;
    workers.reserve(ranges.size());
    for (const auto range : ranges) {
        workers.emplace_back([&, range]() {
            try {
                for (std::size_t index = range.begin; index < range.end; ++index) {
                    records[index] = build_record(index, candidates[index], fixture);
                }
            } catch (const std::exception& error) {
                std::scoped_lock lock(error_mutex);
                worker_errors.push_back(error.what());
            } catch (...) {
                std::scoped_lock lock(error_mutex);
                worker_errors.emplace_back("unknown worker error");
            }
        });
    }
    for (auto& worker : workers) {
        worker.join();
    }
    if (!worker_errors.empty()) {
        std::sort(worker_errors.begin(), worker_errors.end());
        throw std::runtime_error(worker_errors.front());
    }
    BatchRun run;
    run.backend_id = "stage5d-native-cpu-backend-v0";
    run.fixture_id = "stage5d-native-synthetic-shift-fixture-v0";
    run.thread_count = std::max<std::size_t>(1, requested_threads);
    run.candidate_count = candidates.size();
    run.result_count = records.size();
    run.deterministic_ordering = true;
    run.native_cpu_only = true;
    run.cuda_used = false;
    run.gpu_benchmark_performed = false;
    run.solve_claim = false;
    run.records = std::move(records);
    run.output_hash = stable_hash_hex(batch_material(run));
    run.record_hash = stable_hash_hex(run.backend_id + "|" + run.fixture_id + "|" + run.output_hash);
    return run;
}

std::string to_json(const BatchRun& run) {
    std::ostringstream out;
    out << "{\n";
    out << "  \"backend_id\": \"" << json_escape(run.backend_id) << "\",\n";
    out << "  \"fixture_id\": \"" << json_escape(run.fixture_id) << "\",\n";
    out << "  \"thread_count\": " << run.thread_count << ",\n";
    out << "  \"candidate_count\": " << run.candidate_count << ",\n";
    out << "  \"result_count\": " << run.result_count << ",\n";
    out << "  \"output_hash\": \"" << run.output_hash << "\",\n";
    out << "  \"record_hash\": \"" << run.record_hash << "\",\n";
    out << "  \"deterministic_ordering\": true,\n";
    out << "  \"native_cpu_only\": true,\n";
    out << "  \"cuda_used\": false,\n";
    out << "  \"gpu_benchmark_performed\": false,\n";
    out << "  \"solve_claim\": false,\n";
    out << "  \"records\": [\n";
    for (std::size_t index = 0; index < run.records.size(); ++index) {
        const auto& record = run.records[index];
        out << "    {";
        out << "\"candidate_index\": " << record.candidate_index << ", ";
        out << "\"candidate_id\": \"" << json_escape(record.candidate_id) << "\", ";
        out << "\"shift\": " << record.shift << ", ";
        out << "\"output_text\": \"" << json_escape(record.output_text) << "\", ";
        out << "\"output_hash\": \"" << record.output_hash << "\", ";
        out << "\"record_hash\": \"" << record.record_hash << "\"";
        out << "}";
        if (index + 1 < run.records.size()) {
            out << ',';
        }
        out << '\n';
    }
    out << "  ]\n";
    out << "}\n";
    return out.str();
}

}  // namespace libreprimus::native_cpu
