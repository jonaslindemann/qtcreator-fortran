#!/usr/bin/env python3
"""Install the Fortran templates and syntax highlighter for Qt Creator.

Copies the contents of ``templates/`` and ``generic-highlighter/`` into the
Qt Creator user configuration directory:

    Linux/macOS: $XDG_CONFIG_HOME/QtProject/qtcreator (default ~/.config/...)
    Windows:     %APPDATA%\\QtProject\\qtcreator

A manifest of installed files is written so that ``--uninstall`` removes
exactly what was installed and nothing else.

Usage:
    python3 install.py              # install
    python3 install.py --uninstall  # remove installed files
    python3 install.py --dest DIR   # install into a custom directory
    python3 install.py --dry-run    # show what would happen
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

SOURCE_DIR = Path(__file__).resolve().parent
COMPONENTS = ["templates", "generic-highlighter"]
MANIFEST_NAME = ".qtcreator-fortran-manifest.txt"


def default_config_dir():
    """Return the Qt Creator user configuration directory for this platform."""
    if sys.platform.startswith("win"):
        appdata = os.environ.get("APPDATA")
        base = Path(appdata) if appdata else Path.home() / "AppData" / "Roaming"
    else:
        xdg = os.environ.get("XDG_CONFIG_HOME")
        base = Path(xdg) if xdg else Path.home() / ".config"
    return base / "QtProject" / "qtcreator"


def source_files():
    """Yield paths (relative to SOURCE_DIR) of all files to install."""
    for component in COMPONENTS:
        root = SOURCE_DIR / component
        if not root.is_dir():
            sys.exit(f"error: missing source directory {root}")
        for path in sorted(root.rglob("*")):
            if path.is_file():
                yield path.relative_to(SOURCE_DIR)


def install(dest, dry_run=False):
    files = list(source_files())
    print(f"Installing {len(files)} files into {dest}")

    for rel in files:
        target = dest / rel
        action = "update" if target.exists() else "copy"
        print(f"  {action:6} {rel.as_posix()}")
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SOURCE_DIR / rel, target)

    if not dry_run:
        manifest = dest / MANIFEST_NAME
        # Merge with an existing manifest so files from older versions are
        # still removed on uninstall.
        previous = set(read_manifest(dest)) if manifest.exists() else set()
        entries = sorted(previous | {rel.as_posix() for rel in files})
        manifest.write_text("\n".join(entries) + "\n", encoding="utf-8")

    print("Done. Restart Qt Creator to load the Fortran templates.")


def read_manifest(dest):
    manifest = dest / MANIFEST_NAME
    lines = manifest.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip()]


def uninstall(dest, dry_run=False):
    manifest = dest / MANIFEST_NAME
    if manifest.exists():
        entries = read_manifest(dest)
    else:
        print(f"No manifest found in {dest}; using the file list from this checkout.")
        entries = [rel.as_posix() for rel in source_files()]

    print(f"Removing Fortran extension files from {dest}")
    dirs = set()
    for entry in entries:
        target = dest / entry
        if target.is_file():
            print(f"  remove {entry}")
            if not dry_run:
                target.unlink()
        parent = target.parent
        while parent != dest and dest in parent.parents:
            dirs.add(parent)
            parent = parent.parent

    # Remove directories left empty, deepest first. Directories that still
    # hold other content (e.g. Qt Creator's own highlighter downloads) stay.
    for directory in sorted(dirs, key=lambda p: len(p.parts), reverse=True):
        if directory.is_dir() and not any(directory.iterdir()):
            print(f"  rmdir  {directory.relative_to(dest).as_posix()}")
            if not dry_run:
                directory.rmdir()

    if manifest.exists() and not dry_run:
        manifest.unlink()

    print("Done.")


def main():
    parser = argparse.ArgumentParser(
        description="Install Fortran templates and syntax highlighting for Qt Creator."
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=default_config_dir(),
        help="Qt Creator configuration directory (default: %(default)s)",
    )
    parser.add_argument(
        "--uninstall", action="store_true", help="remove previously installed files"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="show what would be done without changing anything"
    )
    args = parser.parse_args()

    dest = args.dest.expanduser().resolve()

    if args.uninstall:
        if not dest.is_dir():
            sys.exit(f"error: {dest} does not exist")
        uninstall(dest, args.dry_run)
    else:
        if not dest.is_dir():
            print(f"Note: {dest} does not exist yet and will be created.")
        install(dest, args.dry_run)


if __name__ == "__main__":
    main()
