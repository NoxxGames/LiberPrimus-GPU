cmake_minimum_required(VERSION 3.26)

project(liberprimus_gpu
    VERSION 0.1.0
    DESCRIPTION "Stage 0A scaffold for a CUDA-accelerated Liber Primus cryptanalysis workbench"
    LANGUAGES CXX
)

option(LPGPU_ENABLE_CUDA "Enable optional CUDA smoke scaffold" OFF)
option(LPGPU_BUILD_TESTS "Build tests" ON)
option(LPGPU_BUILD_CLI "Build command-line smoke executable" ON)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(ProjectOptions)
include(Warnings)
include(CudaConfig)

if(LPGPU_ENABLE_CUDA)
    include(CheckLanguage)
    check_language(CUDA)
    if(NOT CMAKE_CUDA_COMPILER)
        message(FATAL_ERROR "LPGPU_ENABLE_CUDA=ON requires a working CUDA compiler, but CMake could not find one.")
    endif()
    enable_language(CUDA)
    lpgpu_configure_cuda()
endif()

if(LPGPU_BUILD_TESTS)
    include(CTest)
    enable_testing()
endif()

add_subdirectory(src)

if(LPGPU_BUILD_TESTS)
    add_subdirectory(tests)
endif()

if(LPGPU_ENABLE_CUDA)
    add_subdirectory(cuda)
endif()
