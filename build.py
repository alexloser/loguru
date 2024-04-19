#!python3
import sys, os
import py_compile
from setuptools import setup
from Cython.Build import cythonize
from pymagic import (
    file_exist,
    make_directory,
    fullpath,
    base_name,
    copy_tree,
    remove_tree,
)

DISKROOT = fullpath(__file__).split(os.sep)[0]
PROJECTS = DISKROOT + "/PythonProjects"

RELEASE = f"{DISKROOT}/Release/loguru"


DLL_LIST = [
    "loguru/_asyncio_loop.py",
    "loguru/_better_exceptions.py",
    "loguru/_colorama.py",
    "loguru/_colorizer.py",
    "loguru/_contextvars.py",
    "loguru/_ctime_functions.py",
    "loguru/_datetime.py",
    "loguru/_defaults.py",
    "loguru/_error_interceptor.py",
    "loguru/_file_sink.py",
    "loguru/_filters.py",
    "loguru/_get_frame.py",
    "loguru/_handler.py",
    "loguru/_locks_machinery.py",
    "loguru/_recattrs.py",
    "loguru/_simple_sinks.py",
    "loguru/_string_parsers.py",
]

PYC_LIST = [
    "loguru/__init__.py",
    "loguru/_logger.py",
]


def delete_build_cache():
    if file_exist("build"):
        remove_tree("build")
    if file_exist("__pycache__"):
        remove_tree("__pycache__")


def compile_source():
    make_directory(RELEASE)
    sys.argv.append("build")

    setup(ext_modules=cythonize(DLL_LIST, language_level=3, build_dir="build"), zip_safe=False)

    copy_tree("build/lib.win-amd64-cpython-312/loguru", RELEASE)
    for name in PYC_LIST:
        cname = f'{RELEASE}/{base_name(name).replace(".py", ".pyc")}'
        py_compile.compile(name, cfile=cname, optimize=2)


if __name__ == "__main__":
    compile_source()
    delete_build_cache()
