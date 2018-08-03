#!/bin/sh

export PYTHONPATH=wordfinder:${PYTHONPATH}

python -m wordfinder.web.app
