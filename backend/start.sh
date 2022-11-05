#!/bin/bash

brew services start redis
brew services start mongodb/brew/mongodb-community
python __init__.py