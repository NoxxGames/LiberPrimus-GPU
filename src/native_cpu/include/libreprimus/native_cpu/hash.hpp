#pragma once

#include <string>
#include <string_view>

namespace libreprimus::native_cpu {

std::string stable_hash_hex(std::string_view value);

}  // namespace libreprimus::native_cpu
