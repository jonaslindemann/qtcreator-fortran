cmake_minimum_required(VERSION 3.10...3.31)

# Applications started from the macOS Finder don't see the Homebrew PATH, so
# look for gfortran there unless a compiler was chosen by the kit or FC.
if (APPLE AND NOT CMAKE_Fortran_COMPILER AND NOT DEFINED ENV{FC})
    find_program(GFORTRAN_EXECUTABLE gfortran HINTS /opt/homebrew/bin /usr/local/bin)
    if (GFORTRAN_EXECUTABLE)
        set(CMAKE_Fortran_COMPILER "${GFORTRAN_EXECUTABLE}")
    endif()
endif()

project(%{ProjectName} LANGUAGES Fortran)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

file(GLOB fortran_files *.f90)

add_executable(%{ProjectName} ${fortran_files})
