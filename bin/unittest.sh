#!/bin/bash
source bin/config.sh
source $ENV_DIR/bin/activate
if test -z "$1"
then
    python -m unittest discover -s tests
else
    python -m unittest $1
fi
deactivate
