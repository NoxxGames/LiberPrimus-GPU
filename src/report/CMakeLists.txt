add_library(lpgpu_report report_placeholder.cpp)
add_library(libreprimus::report ALIAS lpgpu_report)

target_include_directories(lpgpu_report PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(lpgpu_report PUBLIC lpgpu_project_options PRIVATE lpgpu_project_warnings)
