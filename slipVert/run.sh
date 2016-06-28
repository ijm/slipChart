#!/bin/sh

export PYTHONPATH=../common:$PYTHONPATH

python2.7 plotSlipVert.py -i nasa-slip-vert.dat -o nasa-slip-vert

