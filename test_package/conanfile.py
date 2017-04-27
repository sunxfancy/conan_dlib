from conans import ConanFile, CMake
from conans.tools import os_info, SystemPackageTool
import os

# This easily allows to copy the package in other user or channel
channel = os.getenv("CONAN_CHANNEL", "ci")
username = os.getenv("CONAN_USERNAME", "sunxfancy")
reference = os.getenv("CONAN_REFERENCE", "dlib/19.1.1")
class NanaTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "%s@%s/%s" % (reference, username, channel)
    generators = "cmake"
    def system_requirements(self):
        if os_info.linux_distro == "ubuntu":
            installer = SystemPackageTool()
            # Install the package, will update the package database if pack_name isn't already installed
            installer.install("libjpeg8-dev libpng-dev libx11-dev libxft-dev")
    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def test(self):
        self.run(os.sep.join([".","bin", "dlib_test"]))
