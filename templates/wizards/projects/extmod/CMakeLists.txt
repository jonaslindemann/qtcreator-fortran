cmake_minimum_required(VERSION 3.18...3.31)

# Applications started from the macOS Finder don't see the Homebrew PATH, so
# look for gfortran there unless a compiler was chosen by the kit or FC.
if (APPLE AND NOT CMAKE_Fortran_COMPILER AND NOT DEFINED ENV{FC})
    find_program(GFORTRAN_EXECUTABLE gfortran HINTS /opt/homebrew/bin /usr/local/bin)
    if (GFORTRAN_EXECUTABLE)
        set(CMAKE_Fortran_COMPILER "${GFORTRAN_EXECUTABLE}")
    endif()
endif()

project(%{ProjectName} LANGUAGES C Fortran)

# The Python interpreter with NumPy installed. Select another one with
# -DPython_EXECUTABLE=/path/to/python.
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module NumPy)

set(F2PY_MODULE_NAME "%{ModuleName}")
set(CMAKE_Fortran_MODULE_DIRECTORY "${CMAKE_BINARY_DIR}/modules")
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Constants and implementation: compiled into the extension, but not exposed
# to Python.
add_library(${F2PY_MODULE_NAME}_impl STATIC
    ${F2PY_MODULE_NAME}_const.f90
    ${F2PY_MODULE_NAME}_impl.f90
)
target_include_directories(${F2PY_MODULE_NAME}_impl PUBLIC "${CMAKE_Fortran_MODULE_DIRECTORY}")

# Runtime support code shipped with f2py.
execute_process(
    COMMAND "${Python_EXECUTABLE}" -c "import numpy.f2py; print(numpy.f2py.get_include())"
    OUTPUT_VARIABLE F2PY_INCLUDE_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
    COMMAND_ERROR_IS_FATAL ANY
)
add_library(fortranobject OBJECT "${F2PY_INCLUDE_DIR}/fortranobject.c")
target_link_libraries(fortranobject PUBLIC Python::NumPy)
target_include_directories(fortranobject PUBLIC "${F2PY_INCLUDE_DIR}")

# Generate the C wrapper for the interface module only.
set(F2PY_INTF_SOURCE "${CMAKE_CURRENT_SOURCE_DIR}/${F2PY_MODULE_NAME}_intf.f90")
set(F2PY_OUTPUTS
    "${CMAKE_CURRENT_BINARY_DIR}/${F2PY_MODULE_NAME}module.c"
    "${CMAKE_CURRENT_BINARY_DIR}/${F2PY_MODULE_NAME}-f2pywrappers2.f90"
)
add_custom_command(
    OUTPUT ${F2PY_OUTPUTS}
    COMMAND "${Python_EXECUTABLE}" -m numpy.f2py "${F2PY_INTF_SOURCE}"
            -m ${F2PY_MODULE_NAME} --lower
            --f2cmap "${CMAKE_CURRENT_SOURCE_DIR}/.f2py_f2cmap"
    # Older f2py versions skip wrapper files they don't need.
    COMMAND ${CMAKE_COMMAND} -E touch ${F2PY_OUTPUTS}
    DEPENDS "${F2PY_INTF_SOURCE}" "${CMAKE_CURRENT_SOURCE_DIR}/.f2py_f2cmap"
    WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
    VERBATIM
)

# The Python extension module. After building, run Python from the build
# directory (or add it to PYTHONPATH) and "import %{ModuleName}".
python_add_library(${F2PY_MODULE_NAME} MODULE WITH_SOABI
    ${F2PY_INTF_SOURCE}
    ${F2PY_OUTPUTS}
)
target_link_libraries(${F2PY_MODULE_NAME} PRIVATE fortranobject ${F2PY_MODULE_NAME}_impl)
