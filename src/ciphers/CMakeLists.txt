add_library(lpgpu_ciphers cipher_placeholder.cpp)
add_library(libreprimus::ciphers ALIAS lpgpu_ciphers)

target_include_directories(lpgpu_ciphers PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(lpgpu_ciphers PUBLIC lpgpu_project_options PRIVATE lpgpu_project_warnings)
