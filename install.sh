#!/bin/bash

git clean -f
git reset --hard origin/master
git pull

python3 setup.py py2app
