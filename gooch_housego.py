import logging
from exceptions import ValueError
from glob import glob
import serial
from collections import namedtuple

Status = namedtuple('Status', 'chan mode freq amp phase')

class FreqSynth(object):
        @classmethod
        def probe(cls):
                f = None
                for d in glob('/dev/ttyUSB*'):
                        try:
                                logging.debug("Looking for frequency synthesizer on %s" % d)
                                f = FreqSynth(d)
                                logging.info("Found frequency synthesizer on %s" % d)
                                return f
                        except IOError:
                                pass
                        except Exception as e:
                                logging.error('Unexpected exception: %s' % e)
                        else:
                                break
                if not f:
                        raise RuntimeError("Failed to find device")

        def __init__(self, device='/dev/ttyUSB0'):
                self.device = serial.Serial(device, baudrate=9600, timeout=1)
                # Help auto-baudrate detection
                self.device.write('\n\n\n')
                # Ensure we're talking to the right device
                self.get_status()

        def _write(self, cmd):
                self.device.write(cmd + '\r')

        def select_channel(self, channel):
                self._write('ch%d' % channel)

        def set_frequency(self, freq):
                """ Set the output frequency in MHz """
                if 40 > freq or freq > 150:
                        raise ValueError("Frequency out of range")
                self._write('fr %3.3f' % freq)

        def set_phase(self, phase):
                if 0 > phase or phase > 16383:
                        raise ValueError("Phase out of range")
                self._write('ph %5d' % phase)

        def set_amplitude(self, amp):
                if 0 > amp or amp > 1023:
                        raise ValueError("Amplitude out of range")
                self._write('am %4d' % amp)

        def set_mode(self, mode):
                if mode == 'on':
                        self._write('on')
                elif mode == 'off':
                        self._write('off')
                elif mode == 'mod':
                        self._write('mod')
                else:
                        raise ValueError("Invalid mode")

        def get_status(self):
                self._write('st')
                a = self.device.readline()
                if len(a) == 0: raise IOError('Null status')
                a = a.split()
                if a[0] != 'Ch': raise IOError('Bad status format')

                chan = int(a[1])
                mode = None
                if a[2] == '(off)':
                        mode = 'off'
                elif a[2] == '(on)':
                        mode = 'on'
                elif a[2] == '(mod)':
                        mode = 'mod'

                a = self.device.readline().split()
                if a[0] != "\x00Freq": raise IOError('Bad status format')
                freq = float(a[1])

                a = self.device.readline().split()
                if a[0] != "\x00Amp": raise IOError('Bad status format')
                amp = int(a[1])

                a = self.device.readline().split()
                if a[0] != 'Phase': raise IOError('Bad status format')
                phase = int(a[1])

                return Status(chan, mode, freq, amp, phase)

