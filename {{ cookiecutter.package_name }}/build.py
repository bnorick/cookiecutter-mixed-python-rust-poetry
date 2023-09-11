# Modified from pendulum project with the following LICENSE
# Copyright (c) 2015 Sébastien Eustace

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import os
import shlex
import shutil
import subprocess
import sys
import zipfile

from pathlib import Path

_MATURIN_PATH = None


def get_maturin_path():
    global _MATURIN_PATH

    if _MATURIN_PATH:
        return _MATURIN_PATH

    maturin_path = None
    for path in reversed(sys.path):
        for parent in Path(path).parents:
            possible_path = parent / "bin" / "maturin"
            if possible_path.exists():
                maturin_path = str(possible_path)
                break
        if maturin_path:
            break
    else:
        raise RuntimeError(f"Unable to find maturin, searched parents of {sys.path}")
    _MATURIN_PATH = maturin_path
    return _MATURIN_PATH


def maturin(*args):
    subprocess.call([get_maturin_path(), *list(args)])


def _build():
    build_dir = Path(__file__).parent.joinpath("build")
    build_dir.mkdir(parents=True, exist_ok=True)

    wheels_dir = Path(__file__).parent.joinpath("target/wheels")
    if wheels_dir.exists():
        shutil.rmtree(wheels_dir)

    cargo_args = []
    if os.getenv("MATURIN_BUILD_ARGS"):
        cargo_args = shlex.split(os.getenv("MATURIN_BUILD_ARGS", ""))

    maturin("build", "-r", *cargo_args)

    package_dir = Path(__file__).parent / "src" / "python" / "{{ cookiecutter.package_name }}"

    # We won't use the wheel built by maturin directly since
    # we want Poetry to build it but we need to retrieve the
    # compiled extensions from the maturin wheel.
    wheel = next(iter(wheels_dir.glob("*.whl")))
    with zipfile.ZipFile(wheel.as_posix()) as whl:
        whl.extractall(wheels_dir.as_posix())

        for extension in wheels_dir.rglob("**/*.so"):
            shutil.copyfile(extension, package_dir / extension.name)

    shutil.rmtree(wheels_dir)


def build(setup_kwargs):
    """
    This function is mandatory in order to build the extensions.
    """
    try:
        _build()
    except Exception as e:
        print(
            "  Unable to build Rust extensions, "
            "{{ cookiecutter.package_name }} will use the pure python version of the extensions."
        )
        print(e)


if __name__ == "__main__":
    build({})
