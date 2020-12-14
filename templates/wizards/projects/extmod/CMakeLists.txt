cmake_minimum_required(VERSION 3.5)

project(%{ProjectName})
enable_language(Fortran)

set(LINUX FALSE)
set(BUILD_EXTENSION ON)
set(F2PY_MODULE_NAME "%{ModuleName}")
set(F2PY_IMPL_LIB_NAME "%{ModuleName}_impl")
set(F2PY_INTF_LIB_NAME "%{ModuleName}_intf")

if (UNIX)
    if (NOT APPLE)
        set(LINUX TRUE)
    endif()
endif()

message("-- Checking Python distribution...")
find_package(Python COMPONENTS Interpreter Development)

if (WIN32)
    message("-- Checking for Anaconda...")
    get_filename_component(PYTHON_DIR ${Python_EXECUTABLE} DIRECTORY )
    if (${PYTHON_DIR} MATCHES "anaconda")
        message("-- Anaconda found. Condfiguring f2py...")
        set(CONDA_CMD ${PYTHON_DIR}/condabin/conda.bat)
    else()
        message("-- Anaconda not found. Disable extension build.")
        set(BUILD_EXTENSION OFF)
    endif()
endif()

set(CMAKE_INCLUDE_CURRENT_DIR ON)

file(GLOB FORT_COMMON_SOURCES *.f90)
file(GLOB FORT_INTF_SOURCES *_intf.f90)
file(GLOB FORT_IMPL_SOURCES *_impl.f90)

list(REMOVE_ITEM FORT_COMMON_SOURCES ${FORT_INTF_SOURCES})
list(REMOVE_ITEM FORT_COMMON_SOURCES ${FORT_IMPL_SOURCES})

add_library(${F2PY_IMPL_LIB_NAME} SHARED ${FORT_COMMON_SOURCES} ${FORT_IMPL_SOURCES})
add_library(${F2PY_INTF_LIB_NAME} SHARED ${FORT_COMMON_SOURCES} ${FORT_INTF_SOURCES} ${FORT_IMPL_SOURCES})

if (WIN32)
    message("-- Extension built using Anaconda/F2PY (Windows)...")
    add_custom_command(TARGET ${F2PY_IMPL_LIB_NAME}
        POST_BUILD
        COMMAND ${CONDA_CMD} run python -m numpy.f2py -m ${F2PY_MODULE_NAME} -c ${FORT_COMMON_SOURCES} ${FORT_INTF_SOURCES}  --opt=-O3 -l${F2PY_IMPL_LIB_NAME} -L${CMAKE_BINARY_DIR}
    )
    # COMMAND ${CONDA_CMD} run python -m numpy.f2py -m particle -c ${PROJECT_SOURCE_DIR}/particle_driver.f90 --opt=-O3 -lpartlib -L${CMAKE_BINARY_DIR}
else()
    message("-- Extension module built using f2py...")
    add_custom_command(TARGET ${F2PY_IMPL_LIB_NAME}
        POST_BUILD
        COMMAND f2py -m ${F2PY_MODULE_NAME} -c ${FORT_COMMON_SOURCES} --opt=-O3 -l${F2PY_IMPL_LIB_NAME} -L${CMAKE_BINARY_DIR}
    )
endif()
