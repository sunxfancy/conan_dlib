[![Build status](https://ci.appveyor.com/api/projects/status/lciu4en7tt664ulv?svg=true)](https://ci.appveyor.com/project/MojaveWastelander/conan-dlib)
[![Build Status](https://travis-ci.org/MojaveWastelander/conan_dlib.svg?branch=master)](https://travis-ci.org/MojaveWastelander/conan_dlib)
# conan_dlib

[Conan.io](https://conan.io) package for [dlib](https://github.com/davisking/dlib) library

## Build packages

    $ pip install conan_package_tools
    $ python build.py
    
## Upload packages to server

    $ conan upload dlib/19.1.0@MojaveWastelander/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install dlib/19.1.0@MojaveWastelander/stable

### Package basic test
    $ conan test_package
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    dlib/19.1.0@MojaveWastelander/stable

    [options]
    dlib:iso_cpp_only=True
    
    [generators]
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
