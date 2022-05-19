#!/bin/bash

git clean -f
git reset --hard origin/master

/Users/$USER/Applications/homebrew/bin/python3.9 setup.py py2app

app_destination="/Users/$USER/Documents/LightFilm Project Helper.app"

rm -f "$app_destination"
cp "./dist/LightFilm Project Helper.app" "$app_destination"
