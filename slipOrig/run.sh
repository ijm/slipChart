#!/bin/sh

export PYTHONPATH=../common:$PYTHONPATH

python2.7 plotSlipOrig.py -i nasa-slip-orig.dat -o nasa-slip-orig

