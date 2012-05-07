#!/bin/bash
source env/bin/activate
python -m unittest discover -s tests
deactivate
