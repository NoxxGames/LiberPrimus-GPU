add_library(lpgpu_corpus corpus_placeholder.cpp)
add_library(libreprimus::corpus ALIAS lpgpu_corpus)

target_include_directories(lpgpu_corpus PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(lpgpu_corpus PUBLIC lpgpu_project_options PRIVATE lpgpu_project_warnings)
