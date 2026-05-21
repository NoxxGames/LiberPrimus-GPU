add_library(lpgpu_cuda_smoke
    kernels/cuda_smoke.cu
)
add_library(libreprimus::cuda_smoke ALIAS lpgpu_cuda_smoke)

add_library(lpgpu_cuda_shift_score
    kernels/shift_score_kernel.cu
)
add_library(libreprimus::cuda_shift_score ALIAS lpgpu_cuda_shift_score)

add_library(lpgpu_cuda_gematria_shift_score
    kernels/gematria_shift_score_kernel.cu
)
add_library(libreprimus::cuda_gematria_shift_score ALIAS lpgpu_cuda_gematria_shift_score)

target_include_directories(lpgpu_cuda_smoke
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_include_directories(lpgpu_cuda_shift_score
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_include_directories(lpgpu_cuda_gematria_shift_score
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(lpgpu_cuda_smoke
    PUBLIC
        lpgpu_project_options
)

target_link_libraries(lpgpu_cuda_shift_score
    PUBLIC
        lpgpu_project_options
)

target_link_libraries(lpgpu_cuda_gematria_shift_score
    PUBLIC
        lpgpu_project_options
)

set_target_properties(lpgpu_cuda_smoke PROPERTIES
    CUDA_SEPARABLE_COMPILATION OFF
)

set_target_properties(lpgpu_cuda_shift_score PROPERTIES
    CUDA_SEPARABLE_COMPILATION OFF
)

set_target_properties(lpgpu_cuda_gematria_shift_score PROPERTIES
    CUDA_SEPARABLE_COMPILATION OFF
)

if(LPGPU_BUILD_TESTS)
    add_subdirectory(tests)
endif()
