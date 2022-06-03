#!/bin/bash

git clean -f
git reset --hard origin/master
git pull

/Users/$USER/Applications/homebrew/bin/python3.9 setup.py py2app
