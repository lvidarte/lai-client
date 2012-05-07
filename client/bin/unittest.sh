#!/bin/bash
export PYHTONPATH=$(pwd)/../lai
echo $PYTHONPATH
python -m unittest discover -s tests

