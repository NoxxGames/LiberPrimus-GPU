add_library(lpgpu_core
    version.cpp
    build_config.cpp
)
add_library(libreprimus::core ALIAS lpgpu_core)

target_include_directories(lpgpu_core
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(lpgpu_core
    PUBLIC
        lpgpu_project_options
    PRIVATE
        lpgpu_project_warnings
)

if(LPGPU_ENABLE_CUDA)
    target_compile_definitions(lpgpu_core PRIVATE LPGPU_ENABLE_CUDA=1)
endif()
