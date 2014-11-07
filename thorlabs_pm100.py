from usbtmc import usbtmc

class ThorlabsPM100(object):
    def __init__(self, device):
        self.device = usbtmc(device)
        self.device.write('CONF:POW')
        
    @staticmethod
    def find():
        for dev,name in usbtmc.probe().items():
                if name.startswith('Thorlabs,PM100'):
                        return ThorlabsPM100(dev)
        return None

    def set_wavelength(self, min, max):
        self.device.write('SENSE:CORR:WAVELENGTH MIN %f' % min)
        self.device.write('SENSE:CORR:WAVELENGTH MAX %f' % max)
        
    def read(self):
        self.device.write('READ?')
        return float(self.device.read())
