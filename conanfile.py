# docopt Conan package
# Dmitriy Vetutnev, Odant 2019


from conans import ConanFile, CMake, tools


class docoptConan(ConanFile):
    name = "docopt"
    version = "0.6.2"
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
        "with_unit_tests": [True, False]
    }
    default_options = "with_unit_tests=False"
    generators = "cmake"
    exports_sources = "src/*", "CMakeLists.txt", "fix_tests.patch"
    no_copy_source = True
    build_policy = "missing"

    def source(self):
        tools.patch(patch_file="fix_tests.patch")

    def build(self):
        build_type = "RelWithDebInfo" if self.settings.build_type == "Release" else "Debug"
        cmake = CMake(self, build_type=build_type, msbuild_verbosity='normal')
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
        return
        self.copy("Findtinyxml2.cmake", dst=".", src=".")
        self.copy("tinyxml2.h", dst="include", src="src")
        self.copy("tinyxml2.lib", dst="lib", src="lib")
        self.copy("tinyxml2d.lib", dst="lib", src="lib")
        self.copy("libtinyxml2.a", dst="lib", src="lib")
        self.copy("libtinyxml2d.a", dst="lib", src="lib")
        self.copy("*tinyxml2.pdb", dst="bin", src="src", keep_path=False)
        self.copy("*tinyxml2d.pdb", dst="bin", src="src", keep_path=False)

    def package_id(self):
        self.info.options.with_unit_tests = "any"

    def package_info(self):
        self.cpp_info.libs = ["docopt_s"]
