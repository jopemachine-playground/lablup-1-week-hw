#!/bin/bash

brew services start redis
brew services start mongodb/brew/mongodb-community
cd ./backend
python __init__.py