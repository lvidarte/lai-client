#!/bin/bash
source bin/config.sh
source $ENV_DIR/bin/activate
python -m unittest discover -s tests
deactivate