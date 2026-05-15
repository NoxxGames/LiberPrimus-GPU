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
