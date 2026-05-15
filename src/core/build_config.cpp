#include "libreprimus/build_config.hpp"

namespace libreprimus {

bool cuda_enabled_at_build() {
#if defined(LPGPU_ENABLE_CUDA)
    return true;
#else
    return false;
#endif
}

std::string_view build_mode_summary() {
    return cuda_enabled_at_build() ? "CUDA-enabled Stage 0A build" : "CPU-only Stage 0A build";
}

}  // namespace libreprimus
