# Tests for docopt Conan package
# Dmitriy Vetutnev, Odant 2019


project(PackageTest CXX)
cmake_minimum_required(VERSION 3.0)


include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

enable_testing()


# CONAN_PKG::docopt imported target

add_executable(test_docopt_CONAN_PKG test_docopt.cpp)
target_link_libraries(test_docopt_CONAN_PKG CONAN_PKG::docopt)
set_target_properties(test_docopt_CONAN_PKG
    PROPERTIES
    INSTALL_RPATH "$ORIGIN"
    BUILD_WITH_INSTALL_RPATH True
)
add_test(
    NAME test_docopt_CONAN_PKG
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    COMMAND test_docopt_CONAN_PKG --help
)


# docopt_s imported target

find_package(docopt REQUIRED)
add_executable(test_docopt test_docopt.cpp)
target_link_libraries(test_docopt docopt_s)
set_target_properties(test_docopt
    PROPERTIES
    INSTALL_RPATH "$ORIGIN"
    BUILD_WITH_INSTALL_RPATH True
)
add_test(
    NAME test_docopt
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    COMMAND test_docopt --help
)
