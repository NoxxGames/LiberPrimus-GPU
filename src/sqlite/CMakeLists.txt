add_library(lpgpu_sqlite sqlite_placeholder.cpp)
add_library(libreprimus::sqlite ALIAS lpgpu_sqlite)

target_include_directories(lpgpu_sqlite PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(lpgpu_sqlite PUBLIC lpgpu_project_options PRIVATE lpgpu_project_warnings)
