#!/bin/sh

export PYTHONPATH=wordfinder:${PYTHONPATH}

python -m unittest discover -s test_wordfinder
