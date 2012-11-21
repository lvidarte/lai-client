#!/bin/bash
virtualenv --no-site-packages env
source env/bin/activate
pip install pycrypto==2.6 argparse==1.2.1
deactivate
