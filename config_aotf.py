#!/usr/bin/python

from gooch_housego import FreqSynth

f = FreqSynth('/dev/ttyUSB0')

for ch in [4,7]:
        f.select_channel(ch)
        f.set_mode('mod')
        print 'Channel %d: ' % ch, f.get_status()

