#!/bin/bash
source bin/config.sh
source $ENV_DIR/bin/activate
python lai/server.py
deactivate
