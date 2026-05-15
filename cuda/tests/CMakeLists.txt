add_executable(lpgpu_cuda_smoke_test cuda_smoke_test.cpp)

target_link_libraries(lpgpu_cuda_smoke_test
    PRIVATE
        lpgpu_cuda_smoke
        lpgpu_project_options
        lpgpu_project_warnings
)

add_test(NAME cuda_smoke COMMAND lpgpu_cuda_smoke_test)
