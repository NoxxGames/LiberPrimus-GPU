add_library(lpgpu_project_warnings INTERFACE)

if(MSVC)
    target_compile_options(lpgpu_project_warnings INTERFACE
        $<$<COMPILE_LANGUAGE:CXX>:/W4>
    )
else()
    target_compile_options(lpgpu_project_warnings INTERFACE
        $<$<COMPILE_LANGUAGE:CXX>:-Wall>
        $<$<COMPILE_LANGUAGE:CXX>:-Wextra>
        $<$<COMPILE_LANGUAGE:CXX>:-Wpedantic>
    )
endif()
