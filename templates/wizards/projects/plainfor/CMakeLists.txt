cmake_minimum_required(VERSION 3.5)

project(%{ProjectName} LANGUAGES Fortran)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

add_executable(%{ProjectName} main.f90)
