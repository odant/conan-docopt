# docopt Conan package
# Dmitriy Vetutnev, Odant, 2019


find_path(DOCOPT_INCLUDE_DIR
    NAMES docopt.h
    PATHS ${CONAN_INCLUDE_DIRS_DOCOPT}
    NO_DEFAULT_PATH
)


find_library(DOCOPT_LIBRARY
    NAMES docopt_s libdocopt.a
    PATHS ${CONAN_LIB_DIRS_DOCOPT}
    NO_DEFAULT_PATH
)


include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(docopt
    REQUIRED_VARS DOCOPT_LIBRARY DOCOPT_INCLUDE_DIR
)


if(DOCOPT_FOUND)
    if(NOT TARGET docopt_s)
        add_library(docopt_s STATIC IMPORTED)
        set_target_properties(docopt_s PROPERTIES
            INTERFACE_INCLUDE_DIRECTORIES ${DOCOPT_INCLUDE_DIR}
            IMPORTED_LOCATION ${DOCOPT_LIBRARY}
        )
    endif()
    mark_as_advanced(DOCOPT_INCLUDE_DIR DOCOPT_LIBRARY)
endif()
