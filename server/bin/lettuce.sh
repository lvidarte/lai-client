#!/bin/bash
source bin/config.sh
source $ENV_DIR/bin/activate
lettuce tests
deactivate
