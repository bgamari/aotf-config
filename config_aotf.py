#!/usr/bin/python

import sys
from gooch_housego import FreqSynth

f = FreqSynth('/dev/ttyUSB0')

channels = map(int, sys.argv[1:])
for ch in channels:
        f.select_channel(ch)
        f.set_mode('on')
        print 'Channel %d: ' % ch, f.get_status()

