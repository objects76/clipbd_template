#!/usr/bin/env python3
"""Setup script for clipbd-template with Nuitka compilation support."""

import os
import shutil
import subprocess
import tomllib
from pathlib import Path

from setuptools import find_packages, setup
from setuptools.command.bdist_wheel import bdist_wheel


def get_pyproject_metadata():
    """Extract metadata from pyproject.toml."""
    with (Path(__file__).parent / "pyproject.toml").open("rb") as fp:
        data = tomllib.load(fp)

    project = data["project"]
    return {
        "name": project["name"],
        "version": project["version"],
        "description": project.get("description", ""),
        "requires_python": project.get("requires-python", ">=3.11"),
        "dependencies": project.get("dependencies", []),
    }


# Configure Nuitka via environment variables
os.environ["NUITKA_EXTRA_OPTIONS"] = (
    "--show-progress "
    "--show-memory "
    "--assume-yes-for-downloads "
    "--lto=yes "
    "--python-flag=no_docstrings "
    "--python-flag=no_annotations "
    # Exclude heavy ML libraries from compilation (they stay as Python imports)
    "--nofollow-import-to=torch "
    "--nofollow-import-to=transformers "
    "--nofollow-import-to=openai "
    "--nofollow-import-to=anthropic "
    # Exclude test/dev tools
    "--nofollow-import-to=*.tests "
    "--nofollow-import-to=*.testing "
    "--nofollow-import-to=unittest "
    "--nofollow-import-to=pytest "
    "--nofollow-import-to=ipykernel "
    "--nofollow-import-to=IPython "
    "--nofollow-import-to=jupyter "
    # Anti-bloat plugin to reduce size
    "--enable-plugin=anti-bloat "
)


class BdistWheelCleanup(bdist_wheel):
    """Custom wheel build with cleanup."""

    def run(self):
        super().run()

        # Clean build directory
        build_dir = Path("build")
        if build_dir.exists():
            shutil.rmtree(build_dir)
            print(f"✓ Cleaned {build_dir}")

        # List wheel contents
        wheel_path = next(Path("dist").glob("*.whl"), None)
        if wheel_path:
            print(f"\n✓ Wheel created: {wheel_path}")
            print(f"  Size: {wheel_path.stat().st_size / (1024 * 1024):.2f} MB")
            subprocess.run(["unzip", "-l", str(wheel_path)], check=False)


# Try to import Nuitka build command
try:
    from nuitka.distutils.DistutilCommands import bdist_nuitka as _bdist_nuitka

    class BdistNuitkaCleanup(_bdist_nuitka):
        """Custom Nuitka build with cleanup."""

        def run(self):
            super().run()

            # List wheel contents after build
            wheel_path = next(Path("dist").glob("*.whl"), None)
            if wheel_path:
                print(f"\n✓ Nuitka wheel created: {wheel_path}")
                print(f"  Size: {wheel_path.stat().st_size / (1024 * 1024):.2f} MB")
                subprocess.run(["unzip", "-l", str(wheel_path)], check=False)

    cmd_nuitka = {"bdist_nuitka": BdistNuitkaCleanup}
except ImportError:
    print("Warning: Nuitka not installed. Install with: uv sync --group dev")
    cmd_nuitka = {}


# Get metadata from pyproject.toml
metadata = get_pyproject_metadata()

setup(
    name=metadata["name"],
    version=metadata["version"],
    description=metadata["description"],
    python_requires=metadata["requires_python"],
    install_requires=metadata["dependencies"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "template-paste=main:main",
        ],
    },
    # Nuitka-specific options
    build_with_nuitka=True,
    cmdclass={
        "bdist_wheel": BdistWheelCleanup,
        **cmd_nuitka,
    },
    zip_safe=False,
)
