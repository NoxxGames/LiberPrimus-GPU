#pragma once

#include <cstddef>
#include <vector>

namespace libreprimus::native_cpu {

struct IndexRange {
    std::size_t begin;
    std::size_t end;
};

std::vector<IndexRange> partition_ranges(std::size_t item_count, std::size_t requested_threads);

}  // namespace libreprimus::native_cpu
