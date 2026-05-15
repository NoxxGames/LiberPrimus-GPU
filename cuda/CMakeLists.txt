add_library(lpgpu_cuda_smoke
    kernels/cuda_smoke.cu
)
add_library(libreprimus::cuda_smoke ALIAS lpgpu_cuda_smoke)

target_include_directories(lpgpu_cuda_smoke
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(lpgpu_cuda_smoke
    PUBLIC
        lpgpu_project_options
)

set_target_properties(lpgpu_cuda_smoke PROPERTIES
    CUDA_SEPARABLE_COMPILATION ON
)

if(LPGPU_BUILD_TESTS)
    add_subdirectory(tests)
endif()
