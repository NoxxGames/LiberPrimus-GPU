function(lpgpu_configure_cuda)
    if(NOT DEFINED CMAKE_CUDA_ARCHITECTURES OR CMAKE_CUDA_ARCHITECTURES STREQUAL "")
        set(CMAKE_CUDA_ARCHITECTURES 89 CACHE STRING "CUDA architectures" FORCE)
    endif()

    set(CMAKE_CUDA_STANDARD 20 CACHE STRING "CUDA language standard" FORCE)
    set(CMAKE_CUDA_STANDARD_REQUIRED OFF CACHE BOOL "Require CUDA standard exactly" FORCE)
    set(CMAKE_CUDA_EXTENSIONS OFF CACHE BOOL "Use CUDA compiler extensions" FORCE)
endfunction()
