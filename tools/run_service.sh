#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
py $SCRIPT_DIR/../django/manage.py shell -c "import data.services as s; s.$1()"
