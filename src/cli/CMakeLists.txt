add_executable(lpgpu_cli main.cpp)

target_link_libraries(lpgpu_cli
    PRIVATE
        lpgpu_core
        lpgpu_project_options
        lpgpu_project_warnings
)

set_target_properties(lpgpu_cli PROPERTIES OUTPUT_NAME liberprimus-gpu)
