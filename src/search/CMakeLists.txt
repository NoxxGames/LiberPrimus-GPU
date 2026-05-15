add_library(lpgpu_search search_placeholder.cpp)
add_library(libreprimus::search ALIAS lpgpu_search)

target_include_directories(lpgpu_search PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(lpgpu_search PUBLIC lpgpu_project_options PRIVATE lpgpu_project_warnings)
