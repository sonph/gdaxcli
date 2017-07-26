#!/bin/bash

# Create dummy config file.
[[ ! -e config.py ]] && cp -f config.example.py config.py

pipenv run python *_test.py
