add_library(lpgpu_scoring scoring_placeholder.cpp)
add_library(libreprimus::scoring ALIAS lpgpu_scoring)

target_include_directories(lpgpu_scoring PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(lpgpu_scoring PUBLIC lpgpu_project_options PRIVATE lpgpu_project_warnings)
