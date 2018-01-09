#!/bin/bash
# This script will be used to run tests.

# Get the exact directory of source code.
BASEDIR=$(dirname $(dirname "$0"))

# pep8 has been moved to pycodestyle, but pytest-pep8 has been
# inactive for one year. So we have to use them in parallel.
py.test "$BASEDIR"/tests \
    --pep8 "$BASEDIR"/py_opt_collection \
    --cov "$BASEDIR"/py_opt_collection \
    --cov-report term-missing

echo "================"
echo "PEP8 violations:"
echo "================"
pycodestyle --first "$BASEDIR"/py_opt_collection
echo "================"