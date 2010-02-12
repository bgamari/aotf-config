#!/usr/bin/python

import sys
from gooch_housego import FreqSynth

f = FreqSynth.probe()
channels = range(1,8+1)
on_channels = map(int, sys.argv[1:])
for ch in channels:
        f.select_channel(ch)
	if ch in on_channels:
		f.set_mode('on')
	else:
		f.set_mode('off')
        print 'Channel %d: ' % ch, f.get_status()

