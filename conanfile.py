from conans import ConanFile, CMake
from conans.tools import unzip, download, replace_in_file, os_info, SystemPackageTool
import os

class DLibConan(ConanFile):
    name = "dlib"
    generators = "cmake"
    version = "19.2.0"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "iso_cpp_only" : [True, False], "use_blas" : [True, False], "use_lapack": [True, False], "enable_gif" : [True, False], "enable_png" : [True, False], "enable_jpeg" : [True, False], "no_gui_support" : [True, False], "enable_stack_trace" : [True, False], "link_with_sqlite" : [True, False],    "enable_asserts" : [True, False]}

    # keep default options as in library
    default_options = "shared=False", "iso_cpp_only=True", "use_blas=False", "use_lapack=False", "enable_gif=True", "enable_png=True", "enable_jpeg=True", "no_gui_support=True", "enable_stack_trace=False", "link_with_sqlite=True", "enable_asserts=False"
    license = "Boost"
    url = "https://github.com/sunxfancy/conan_dlib"

    source_folder_name = "dlib-19.2"
    file_name = "v19.2.tar.gz"
    download_url = "https://github.com/davisking/dlib/archive/"+file_name

    def source(self):
        download(self.download_url, self.file_name)
        unzip(self.file_name)
        os.unlink(self.file_name)
        if os.path.exists('dlib'):
            os.unlink('dlib')
        os.rename(self.source_folder_name, 'dlib')
        replace_in_file("dlib/dlib/CMakeLists.txt", 'project(dlib)', '''project(dlib)
include(../../conanbuildinfo.cmake)
conan_basic_setup()
''')
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
        cmake = CMake(self)
        print("Compiler: %s %s" % (self.settings.compiler, self.settings.compiler.version))
        print("Arch: %s" % self.settings.arch)

        lib_opt = []

        if self.options.iso_cpp_only: # will override all other options
            lib_opt.append("-DDLIB_ISO_CPP_ONLY=TRUE")
        else:
            if self.options.enable_gif:
                lib_opt.append("-DDLIB_GIF_SUPPORT=TRUE")

            if self.options.enable_png:
                lib_opt.append("-DDLIB_PNG_SUPPORT=TRUE")

            if self.options.enable_jpeg:
                lib_opt.append("-DDLIB_JPEG_SUPPORT=TRUE")

            if self.options.link_with_sqlite:
                lib_opt.append("-DDLIB_LINK_WITH_SQLITE3=TRUE")

            if self.options.use_blas:
                lib_opt.append("-DLIB_USE_BLAS=TRUE")
            else:
                lib_opt.append("-DLIB_USE_BLAS=FALSE")

            if self.options.use_lapack:
                lib_opt.append("-DLIB_USE_LAPACK=TRUE")
            else:
                lib_opt.append("-DLIB_USE_LAPACK=FALSE")

        if self.options.no_gui_support:
            lib_opt.append("-DDLIB_NO_GUI_SUPPORT=TRUE")

        if self.options.enable_stack_trace:
            lib_opt.append("-DDLIB_ENABLE_STACK_TRACE=TRUE")

        if self.options.enable_asserts:
            lib_opt.append("-DDLIB_ENABLE_ASSERTS=TRUE")

        os.mkdir('build')
        cmake.configure(lib_opt, build_dir="build", source_dir=os.path.join(self.source_folder, "dlib"))
        cmake.build()

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
