#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export PIPENV_PIPFILE=$SCRIPT_DIR/../django/Pipfile

# alternatively use the django-extensions runscript command
py $SCRIPT_DIR/../django/manage.py shell -c "import soodud.services as s; s.$1()"
