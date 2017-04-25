from conan.packager import ConanMultiPackager
import os

if __name__ == "__main__":
    builder = ConanMultiPackager(args='--build=missing', username="sunxfancy")
    builder.add_common_builds(pure_c=False)
    if os.environ["APPVEYOR_BUILD_WORKER_IMAGE"] == "Visual Studio 2017":
        builder.builds[0]["compiler.version"] = 15
    else:
        builder.builds[0]["compiler.version"] = 14
    builder.run()
