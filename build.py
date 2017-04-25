from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(args='--build=missing', username="sunxfancy", default_visual_versions=['14', '15'])
    builder.add_common_builds(pure_c=False)
    builder.run()
