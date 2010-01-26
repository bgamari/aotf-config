import serial
from exceptions import ValueError

class FreqSynth(object):
        def __init__(self, device='/dev/ttyUSB0'):
                self.device = serial.Serial(device, timeout=1)
		# Ensure we're talking to the right device
		self.get_status()

        def _write(self, cmd):
                self.device.write(cmd + '\r')

	def select_channel(self, channel):
                self._write('ch%d' % channel)

        def set_frequency(self, freq):
                """ Set the output frequency in MHz """
                if not 40 < freq < 150:
                        raise ValueError("Frequency out of range")
                self._write('fr %3.3f' % freq)

        def set_phase(self, phase):
                if not 0 < phase < 16383:
                        raise ValueError("Phase out of range")
                self._write('ph %5d' % phase)

        def set_amplitude(self, amp):
                if not 0 < amp < 1023:
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
                a = self.device.readline().split()
                if a[0] != 'Ch': raise Exception('Bad status format')

                chan = int(a[1])
                mode = None
                if a[2] == '(off)':
                        mode = 'off'
                elif a[2] == '(on)':
                        mode = 'on'
                elif a[2] == '(mod)':
                        mode = 'mod'

                a = self.device.readline().split()
                if a[0] != "\x00Freq": raise Exception()
                freq = float(a[1])

                a = self.device.readline().split()
                if a[0] != "\x00Amp": raise Exception
                amp = int(a[1])

                a = self.device.readline().split()
                if a[0] != 'Phase': raise Exception()
                phase = int(a[1])

                return chan, mode, freq, amp, phase

