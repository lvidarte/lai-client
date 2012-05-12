#!/bin/bash
source bin/config.sh
source $ENV_DIR/bin/activate
python lai/client.py "$@"
deactivate
