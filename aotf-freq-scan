#!/usr/bin/python

import os

"""
Scan the AOTF drive frequency of the given channel through the given band,
recording the power from a Thorlabs DM100 power meter at every frequency
"""

configs = {           # (chan, min_f, max_f)
        'green':        (1, 68.5, 70.5),
        'red':          (2, 51.5, 55.5),
}

class usbtmc(object):
        """Simple implementation of a USBTMC device driver, in the style of visa.h"""

        def __init__(self, device):
                self.device = device
                self.FILE = os.open(device, os.O_RDWR)

        def write(self, command):
                os.write(self.FILE, command);

        def read(self, length = 4000):
                return os.read(self.FILE, length)

        def get_name(self):
                self.write("*IDN?")
                return self.read(300)

        def send_reset(self):
                self.write("*RST")


def plot(data):
        from matplotlib import pyplot as pl
        freqs = np.unique(data['f'])
        powers = [ data[data['f'] == f]['p'] for f in freqs ]
        means = [ np.mean(p) for p in powers ]
        stds = [ np.std(p) for p in powers ]

        pl.errorbar(x=freqs, y=means, yerr=stds, fmt='.')
        pl.xlabel('Frequency (MHz)')
        pl.ylabel('Relative transmitted power')

        max_i = np.argmax(abs(data['p']))
        m = data[max_i]
        pl.axvline(x=m['f'])
        pl.figtext(0.6, 0.8, 'Maximum: %2.3f MHz' % m['f'])

        pl.show()

if __name__ == '__main__':
        import sys, time
        import numpy as np
        from gooch_housego import FreqSynth
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--plot', action='store_true', help='Plot')
        parser.add_argument('-o', '--output', type=file, help='Output to file')
        parser.add_argument('-s', '--step', type=float, metavar='FREQ', help='Scan step size in MHz', default=0.010)
        parser.add_argument('-l', '--lower', type=float, metavar='FREQ', help='Beginning of scan in MHz')
        parser.add_argument('-b', '--upper', type=float, metavar='FREQ', help='End of scan in MHz')
        parser.add_argument('-c', '--channel', type=int, metavar='N', help='AOTF channel to scan')
        parser.add_argument('-P', '--preset', metavar='NAME', help='Select a preset scan configuration')
        parser.add_argument('-w', '--wait', type=float, metavar='TIME', help='Duration to wait between data points', default=1e-3)
        parser.add_argument('-S', '--samples', type=int, metavar='N', help='Number of samples to take for each frequency', default=5)
        args = parser.parse_args()

        chan = args.channel
        lower = args.lower
        upper = args.upper

        if args.preset is None:
                pass
        elif args.preset in presets:
                chan,lower,upper = presets[args.preset]
        else:
                parser.error("Unknown preset configuration '%s'" % args.preset)

        test = usbtmc('/dev/usbtmc0')
        test.write('CONF:POW')

        synth = FreqSynth.probe()
        synth.select_channel(channel)
        synth.set_mode('on')

        data = []
        for freq in np.arange(min_freq, max_freq, step_freq):
                synth.set_frequency(freq)
                time.sleep(args.wait)
                for i in range(args.samples):
                        test.write('READ?')
                        val = float(test.read())
                        data.append((freq, val))

        args.output.close()
        data = np.array(data, dtype=[('f', 'f8'), ('p', 'f8')])

        max_i = np.argmax(abs(data['p']))
        print 'Maximum at %3.3f MHz' % data['p'][max_i]

        if args.output is not None:
                args.output.write('# Time (seconds)\tPower (Watts)\n')
                np.savetxt(args.output, data, '%3.5e')

        if args.plot:
                plot(data)

