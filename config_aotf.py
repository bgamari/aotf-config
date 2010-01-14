#!/usr/bin/python

from gooch_housego import FreqSynth

f = FreqSynth('/dev/ttyUSB0')
f.select_channel(0)
f.set_mode('mod')

