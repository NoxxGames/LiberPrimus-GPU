add_library(lpgpu_native_cpu
    hash.cpp
    native_batch.cpp
    threading.cpp
)
add_library(libreprimus::native_cpu ALIAS lpgpu_native_cpu)

target_include_directories(lpgpu_native_cpu
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(lpgpu_native_cpu
    PUBLIC
        lpgpu_project_options
    PRIVATE
        lpgpu_project_warnings
)

add_executable(lpgpu_native_cpu_backend_cli native_cpu_backend_cli.cpp)
target_link_libraries(lpgpu_native_cpu_backend_cli
    PRIVATE
        lpgpu_native_cpu
        lpgpu_project_options
        lpgpu_project_warnings
)
