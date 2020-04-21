# docopt Conan package
# Dmitriy Vetutnev, Odant 2019 - 2020


from conans import ConanFile, CMake, tools


class docoptConan(ConanFile):
    name = "docopt"
    version = "0.6.2+1"
    license = "MIT https://github.com/docopt/docopt.cpp/blob/master/LICENSE-MIT"
    description = "docopt creates beautiful command-line interfaces"
    url = "https://github.com/odant/conan-docopt"
    settings = {
        "os": ["Windows", "Linux"],
        "compiler": ["Visual Studio", "gcc"],
        "build_type": ["Debug", "Release"],
        "arch": ["x86", "x86_64", "mips"]
    }
    options = {
        "with_unit_tests": [True, False],
        "ninja": [True, False]
    }
    default_options = "with_unit_tests=False", "ninja=True"
    generators = "cmake"
    exports_sources = "src/*", "CMakeLists.txt", "fix_tests.patch", "fix_MSVC_2019.patch", "Finddocopt.cmake"
    no_copy_source = True
    build_policy = "missing"

    def build_requiments(self):
        if self.options.ninja:
            self.build_requires("ninja_installer/1.9.0@bincrafters/stable")

    def source(self):
        tools.patch(patch_file="fix_tests.patch")
        tools.patch(patch_file="fix_MSVC_2019.patch")

    def build(self):
        build_type = "RelWithDebInfo" if self.settings.build_type == "Release" else "Debug"
        gen = "Ninja" if self.options.ninja == True else None
        cmake = CMake(self, build_type=build_type, generator=gen, msbuild_verbosity='normal')
        cmake.verbose = True
        if self.options.with_unit_tests:
            cmake.definitions["WITH_TESTS"] = "ON"
        cmake.configure()
        cmake.build()
        if self.options.with_unit_tests:
            if cmake.is_multi_configuration:
                self.run("ctest --verbose --build-config %s" % build_type)
            else:
                self.run("ctest --verbose")

    def package(self):
        self.copy("Finddocopt.cmake", dst=".", src=".")
        self.copy("docopt.h", dst="include", src="src")
        self.copy("docopt_value.h", dst="include", src="src")
        self.copy("docopt_s.lib", dst="lib", src="lib")
        self.copy("docopt_s.pdb", dst="bin", src="lib")
        self.copy("libdocopt.a", dst="lib", src="lib")

    def package_id(self):
        self.info.options.with_unit_tests = "any"
        self.info.options.ninja = "any"

    def package_info(self):
        self.cpp_info.libs = ["docopt_s"]
