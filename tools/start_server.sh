#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export PIPENV_PIPFILE=$SCRIPT_DIR/../django/Pipfile

pipenv run py $SCRIPT_DIR/../django/manage.py runserver 8001
