#!/bin/bash
cp -f config.py config.example.py  # Create dummy config file.
pipenv run python *_test.py
