add_executable(lpgpu_smoke_core_test smoke_core_test.cpp)

target_link_libraries(lpgpu_smoke_core_test
    PRIVATE
        lpgpu_core
        lpgpu_corpus
        lpgpu_gematria
        lpgpu_ciphers
        lpgpu_scoring
        lpgpu_search
        lpgpu_report
        lpgpu_sqlite
        lpgpu_project_options
        lpgpu_project_warnings
)

add_test(NAME smoke_core COMMAND lpgpu_smoke_core_test)

add_executable(lpgpu_native_cpu_backend_test ../../tests/cpp/native_cpu_backend_tests.cpp)
target_link_libraries(lpgpu_native_cpu_backend_test
    PRIVATE
        lpgpu_native_cpu
        lpgpu_project_options
        lpgpu_project_warnings
)
add_test(NAME native_cpu_backend COMMAND lpgpu_native_cpu_backend_test)

add_executable(lpgpu_native_cpu_threading_test ../../tests/cpp/native_cpu_threading_tests.cpp)
target_link_libraries(lpgpu_native_cpu_threading_test
    PRIVATE
        lpgpu_native_cpu
        lpgpu_project_options
        lpgpu_project_warnings
)
add_test(NAME native_cpu_threading COMMAND lpgpu_native_cpu_threading_test)
