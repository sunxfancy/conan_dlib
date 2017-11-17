from conans import ConanFile, CMake
from conans.tools import unzip, replace_in_file, os_info, SystemPackageTool

class DLibConan(ConanFile):
    name = "dlib"
    generators = "cmake"
    version = "19.1.2"
    settings = "os", "compiler", "build_type", "arch"
    options = {"iso_cpp_only" : [True, False], "build_PIC" : [True, False], "use_blas" : [True, False], "use_lapack": [True, False], "enable_gif" : [True, False], "enable_png" : [True, False], "enable_jpeg" : [True, False], "no_gui_support" : [True, False], "enable_stack_trace" : [True, False], "link_with_sqlite" : [True, False],    "enable_asserts" : [True, False]}

    # keep default options as in library
    default_options = "iso_cpp_only=True", "build_PIC=False", "use_blas=False", "use_lapack=False", "enable_gif=True", "enable_png=True", "enable_jpeg=True", "no_gui_support=True", "enable_stack_trace=False", "link_with_sqlite=True", "enable_asserts=False"
    license = "Boost"
    url = "https://github.com/sunxfancy/conan_dlib"

    def source(self):
        self.run("git config --global http.sslVerify false")
        self.run("git clone https://github.com/davisking/dlib.git --depth=1")

    def requirements(self):
        if not self.options.iso_cpp_only:
            if self.options.enable_gif:
                self.requires("giflib/5.1.3@lasote/stable")

            if self.options.enable_png:
                self.requires("libpng/1.6.21@lasote/stable")

            if self.options.enable_jpeg:
                self.requires("libjpeg-turbo/1.4.2@lasote/stable")

            if self.options.link_with_sqlite:
                self.requires("sqlite3/3.14.1@rdeterre/stable")

    def build(self):
        cmake = CMake(self.settings)
        print("Compiler: %s %s" % (self.settings.compiler, self.settings.compiler.version))
        print("Arch: %s" % self.settings.arch)

        lib_opt = ""

        if self.options.iso_cpp_only: # will override all other options
            lib_opt = " -DDLIB_ISO_CPP_ONLY=TRUE"
        else:
            if self.options.enable_gif:
                lib_opt += " -DDLIB_GIF_SUPPORT=TRUE"

            if self.options.enable_png:
                lib_opt += " -DDLIB_PNG_SUPPORT=TRUE"

            if self.options.enable_jpeg:
                lib_opt += " -DDLIB_JPEG_SUPPORT=TRUE"

            if self.options.link_with_sqlite:
                lib_opt += " -DDLIB_LINK_WITH_SQLITE3=TRUE"

            if self.options.use_blas:
                lib_opt += " -DLIB_USE_BLAS=TRUE"
            else:
                lib_opt += " -DLIB_USE_BLAS=FALSE"

            if self.options.use_lapack:
                lib_opt += " -DLIB_USE_LAPACK=TRUE"
            else:
                lib_opt += " -DLIB_USE_LAPACK=FALSE"

        if self.options.no_gui_support:
            lib_opt = " -DDLIB_NO_GUI_SUPPORT=TRUE"

        if self.options.enable_stack_trace:
            lib_opt = " -DDLIB_ENABLE_STACK_TRACE=TRUE"

        if self.options.enable_asserts:
            lib_opt = " -DDLIB_ENABLE_ASSERTS=TRUE"

        if self.options.build_PIC:
            lib_opt += " -DCMAKE_CXX_FLAGS=-fPIC"

        replace_in_file("dlib/dlib/CMakeLists.txt", 'project(dlib)', '''project(dlib)
include(../../conanbuildinfo.cmake)
conan_basic_setup()
''')

        self.run("mkdir build")
        self.run('cd build && cmake ../dlib %s %s' % (cmake.command_line, lib_opt))
        self.run("cd build && cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include/dlib", src="dlib/dlib")
        self.copy("config.h", dst="include/dlib", src="build/dlib")
        self.copy("revision.h", dst="include/dlib", src="build/dlib")
        self.copy("*.lib", dst="lib", src="build/dlib/Release")
        self.copy("*.lib", dst="lib", src="build/dlib/Debug")
        self.copy("*.lib", dst="lib", src="build/dlib/lib")
        self.copy("*.so", dst="lib", src="build/dlib/lib")
        self.copy("*.a", dst="lib", src="build/dlib/lib")

    def package_info(self):
        print("Compiler: %s %s" % (self.settings.compiler, self.settings.compiler.version))
        print("Arch: %s" % self.settings.arch)
        print("Build_type: %s" % self.settings.build_type)
        if self.settings.compiler == "Visual Studio":
            print("Runtime: %s" % self.settings.compiler.runtime)
        self.cpp_info.libs = ["dlib"]
        if os_info.is_macos:
            self.cpp_info.libs.append("cblas")
            self.cpp_info.libs.append("clapack")
