#!/usr/bin/python

import sys
from glob import glob
from gooch_housego import FreqSynth

f = None
for d in glob('/dev/ttyUSB*'):
	try:
		f = FreqSynth(d)
	except:
		pass
	else:
		break

if not f:
	raise Exception("Failed to find device")

channels = range(1,8)
on_channels = map(int, sys.argv[1:])
for ch in channels:
        f.select_channel(ch)
	if ch in on_channels:
		f.set_mode('on')
	else:
		f.set_mode('off')
        print 'Channel %d: ' % ch, f.get_status()

