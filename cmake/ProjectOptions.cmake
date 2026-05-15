add_library(lpgpu_project_options INTERFACE)
target_compile_features(lpgpu_project_options INTERFACE cxx_std_20)

if(MSVC)
    target_compile_options(lpgpu_project_options INTERFACE
        $<$<COMPILE_LANGUAGE:CXX>:/permissive->
        $<$<COMPILE_LANGUAGE:CXX>:/Zc:__cplusplus>
    )
endif()
