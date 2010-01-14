import serial
from exceptions import ValueError

class FreqSynth(object):
        def __init__(self, device='/dev/ttyUSB0'):
                self.device = serial.Serial(device)

	def select_channel(self, channel):
                self.device.write('ch%d\n' % channel)

        def set_frequency(self, freq):
                """ Set the output frequency in MHz """
                if not 40 < freq < 150:
                        raise ValueError("Frequency out of range")
                self.device.write('fr %3.3f\n' % freq)

        def set_phase(self, phase):
                if not 0 < phase < 16383:
                        raise ValueError("Phase out of range")
                self.device.write('ph %5d\n' % phase)

        def set_amplitude(self, amp):
                if not 0 < amp < 1023:
                        raise ValueError("Amplitude out of range")
                self.device.write('am %4d\n' % amp)

        def set_mode(self, mode):
                if mode == 'on':
                        self.device.write('on\n')
                elif mode == 'off':
                        self.device.write('off\n')
                elif mode == 'mod':
                        self.device.write('mod\n')
                else:
                        raise ValueError("Invalid mode")

