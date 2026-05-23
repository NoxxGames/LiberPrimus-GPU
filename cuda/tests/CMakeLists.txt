add_executable(lpgpu_cuda_smoke_test cuda_smoke_test.cpp)
add_executable(lpgpu_cuda_shift_score_test shift_score_kernel_test.cpp)
add_executable(lpgpu_cuda_gematria_shift_score_test gematria_shift_score_kernel_test.cpp)
add_executable(lpgpu_cuda_gematria_shift_score_stage5m_runner gematria_shift_score_stage5m_runner.cpp)
add_executable(lpgpu_cuda_prime_minus_one_stream_test prime_minus_one_stream_kernel_test.cpp)
add_executable(lpgpu_cuda_prime_minus_one_bounded_p56_stage5ad_test prime_minus_one_bounded_p56_stage5ad_test.cpp)

target_link_libraries(lpgpu_cuda_smoke_test
    PRIVATE
        lpgpu_cuda_smoke
        lpgpu_project_options
        lpgpu_project_warnings
)

target_link_libraries(lpgpu_cuda_shift_score_test
    PRIVATE
        lpgpu_cuda_shift_score
        lpgpu_project_options
        lpgpu_project_warnings
)

target_link_libraries(lpgpu_cuda_gematria_shift_score_test
    PRIVATE
        lpgpu_cuda_gematria_shift_score
        lpgpu_project_options
        lpgpu_project_warnings
)

target_link_libraries(lpgpu_cuda_gematria_shift_score_stage5m_runner
    PRIVATE
        lpgpu_cuda_gematria_shift_score
        lpgpu_project_options
        lpgpu_project_warnings
)

target_link_libraries(lpgpu_cuda_prime_minus_one_stream_test
    PRIVATE
        lpgpu_cuda_prime_minus_one_stream
        lpgpu_project_options
        lpgpu_project_warnings
)

target_link_libraries(lpgpu_cuda_prime_minus_one_bounded_p56_stage5ad_test
    PRIVATE
        lpgpu_cuda_prime_minus_one_stream
        lpgpu_project_options
        lpgpu_project_warnings
)

add_test(NAME cuda_smoke COMMAND lpgpu_cuda_smoke_test)
add_test(NAME cuda_shift_score_synthetic COMMAND lpgpu_cuda_shift_score_test)
add_test(NAME cuda_gematria_shift_score_synthetic COMMAND lpgpu_cuda_gematria_shift_score_test)
add_test(NAME cuda_prime_minus_one_stream_synthetic COMMAND lpgpu_cuda_prime_minus_one_stream_test)
add_test(NAME cuda_prime_minus_one_bounded_p56_stage5ad COMMAND lpgpu_cuda_prime_minus_one_bounded_p56_stage5ad_test)
