#pragma once

#include <string_view>

namespace libreprimus {

bool cuda_enabled_at_build();
std::string_view build_mode_summary();

}  // namespace libreprimus
