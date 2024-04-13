#!/bin/sh

export PYTHONPATH=../common:$PYTHONPATH

python plotSlipOrig.py -i nasa-slip-orig.dat -o nasa-slip-orig

