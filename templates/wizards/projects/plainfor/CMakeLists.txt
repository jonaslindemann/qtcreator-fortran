cmake_minimum_required(VERSION 3.5)

project(%{ProjectName} LANGUAGES Fortran)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

file(GLOB fortran_files *.f90)

add_executable(%{ProjectName} ${fortran_files})
