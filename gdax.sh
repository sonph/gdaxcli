#!/bin/bash
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pushd "$script_dir" > /dev/null 2>&1

pipenv run python gdaxcli.py "$@"
