"""
py2app/py2exe build script for lightfilm_project_helper.

Usage (Mac OS X):
    python3 setup.py py2app
"""

from setuptools import setup

APP = ['lightfilm_project_helper.py']
DATA_FILES = ['main.cfg']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['glob', 're', 'distutils', 'pickle', 'PyQt5']
}

setup(
    app=APP,
    data_files=DATA_FILES,
    name="LightFilm Project Helper",
    options={'py2app': OPTIONS},
    setup_requires=['py2app']
)
