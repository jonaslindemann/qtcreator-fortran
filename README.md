# Templates for using Qt Creator and Fortran

This project adds support for Fortran projects and source files in Qt Creator as well as syntax-highlighting.

# Installation

## Using the install script (all platforms)

Clone or download this repository and run the install script with Python 3:

	python3 install.py

This copies the templates and syntax highlighter into the Qt Creator user configuration directory (**~/.config/QtProject/qtcreator** on Linux/macOS, **%APPDATA%\QtProject\qtcreator** on Windows). Restart Qt Creator afterwards.

Other options:

	python3 install.py --dry-run      # show what would be installed
	python3 install.py --dest DIR     # install into a custom configuration directory
	python3 install.py --uninstall    # remove the installed files

## Manual installation on Linux/macOS

Go to the user configuration directory of Qt Creator

	cd ~/.config/QtProject/qtcreator

Download this archive:

	wget https://github.com/jonaslindemann/qtcreator-fortran/archive/master.zip

Unzip the archive:

	unzip master.zip
	mv qtcreator-fortran-master/* .

Restart Qt Creator.

## Manual installation on Windows

Open the **%appdata%\QtProject\qtcreator** folder in explorer.

Download this archive into the above folder:

	wget https://github.com/jonaslindemann/qtcreator-fortran/archive/master.zip

Open the zip-file and go into the **qtcreator-fortran-master** folder in the zip file. Select all files and press **Ctrl+C**. Paste the files in the **%appdata%\QtProject\qtcreator** folder. 

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



