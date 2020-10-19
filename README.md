# Templates for using Qt Creator and Fortran

This project adds support for Fortran projects and source files in Qt Creator as well as syntax-highlighting.

# Installation

Go to the user configuration directory of Qt Creator

	cd ~/.config/QtProject/qtcreator

Download this archive:

	wget https://github.com/jonaslindemann/qtcreator-fortran/archive/master.zip

Unzip the archive:

	unzip master.zip
	mv qtcreator-fortran-master/* .

Restart Qt Creator.

# Usage

When installed Qt Creator can create a CMake based Fortran project as well as create Fortran source files and modules.

## Create a Fortran project

1. Select **File/New File or Project...**
2. Select **Non-Qt Project**
3. Select **Plain Fortran Application**
4. Click **Choose...** 

Follow the wizard for the rest of the setup.

## Adding a Fortran source code

1. Select **File/New File or Project...**
2. Select **Fortran** from **Files and Classes**.
3. Select **Fortran Source File**.
4. Click **Choose...**

Follow the wizard for the rest of the setup.

## Adding a Fortran module

1. Select **File/New File or Project...**
2. Select **Fortran** from **Files and Classes**.
3. Select **Fortran Nodule File**.
4. Click **Choose...**

Follow the wizard for the rest of the setup.



