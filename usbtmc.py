#!/usr/bin/python

import os

def probe():
        from glob import glob
        devices = {}
        for dev in glob('/dev/usbtmc*'):
                try:
                        d = usbtmc(dev)
                        devices[dev] = d.get_name()
                except Exception as e:
                        print 'Failed to probe device %s: %s' % (dev, e)
        return devices

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
