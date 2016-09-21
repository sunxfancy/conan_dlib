project(dlib_test)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(dlib_test krr_classification_ex.cpp)
target_link_libraries(dlib_test ${CONAN_LIBS})

if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU" OR "${CMAKE_CXX_COMPILER_ID}" STREQUAL "CLANG")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
  target_link_libraries(dlib_test X11 Xft pthread)					
endif()