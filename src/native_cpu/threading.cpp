#include "libreprimus/native_cpu/threading.hpp"

#include <algorithm>

namespace libreprimus::native_cpu {

std::vector<IndexRange> partition_ranges(std::size_t item_count, std::size_t requested_threads) {
    const std::size_t worker_count = std::max<std::size_t>(1, requested_threads);
    std::vector<IndexRange> ranges;
    ranges.reserve(worker_count);
    const std::size_t base = item_count / worker_count;
    const std::size_t remainder = item_count % worker_count;
    std::size_t begin = 0;
    for (std::size_t index = 0; index < worker_count; ++index) {
        const std::size_t width = base + (index < remainder ? 1 : 0);
        ranges.push_back(IndexRange{begin, begin + width});
        begin += width;
    }
    return ranges;
}

}  // namespace libreprimus::native_cpu
