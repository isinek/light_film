#!/bin/bash

git clean -f
git reset --hard origin/master

/Users/$USER/Applications/homebrew/bin/python3.9 setup.py py2app

mv "./dist/LightFilm Project Helper" ../
