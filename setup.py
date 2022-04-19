"""
py2app/py2exe build script for lightfilm_project_helper.

Usage (Mac OS X):
    python setup.py py2app

Usage (Windows):
    python setup.py py2exe
"""

import sys
from setuptools import setup

APP = ['lightfilm_project_helper.py']

if sys.platform == 'darwin':
    extra_options = dict(
        setup_requires=['py2app'],
        # Cross-platform applications generally expect sys.argv to
        # be used for opening files.
        # Don't use this with GUI toolkits, the argv
        # emulator causes problems and toolkits generally have
        # hooks for responding to file-open events.
        options=dict(py2app=dict(argv_emulation=True)),
    )
elif sys.platform == 'win32':
    extra_options = dict(
        setup_requires=['py2exe']
    )
else:
    extra_options = dict()

setup(
    app=APP,
    name="LightFilm Project Helper",
    **extra_options
)

