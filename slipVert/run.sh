#!/bin/sh

export PYTHONPATH=../common:$PYTHONPATH

python plotSlipVert.py -i nasa-slip-vert.dat -o nasa-slip-vert

