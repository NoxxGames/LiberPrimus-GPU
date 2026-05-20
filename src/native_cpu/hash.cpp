#include "libreprimus/native_cpu/hash.hpp"

#include <array>
#include <cstdint>
#include <iomanip>
#include <sstream>

namespace libreprimus::native_cpu {

namespace {

constexpr std::uint64_t fnv_prime = 1099511628211ULL;

std::uint64_t fnv1a(std::string_view value, std::uint64_t seed) {
    std::uint64_t hash = seed;
    for (const unsigned char ch : value) {
        hash ^= static_cast<std::uint64_t>(ch);
        hash *= fnv_prime;
    }
    return hash;
}

}  // namespace

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

}  // namespace libreprimus::native_cpu
