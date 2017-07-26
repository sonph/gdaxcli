#!/bin/bash
cp -f config.example.py config.py  # Create dummy config file.
pipenv run python *_test.py
