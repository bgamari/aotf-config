#!/usr/bin/python

from gooch_housego import FreqSynth
import gtk
import sys, os
import logging

resource_prefix=os.path.join(sys.prefix, 'local', 'share', 'aotf-config')

logging.basicConfig(level=logging.DEBUG)

class AotfChannel(object):
        def __init__(self, n, device):
                self.device = device
                self.n = n
                self.builder = gtk.Builder()
                self.builder.add_from_file(os.path.join(resource_prefix, 'aotf-channel.glade'))
                self.builder.connect_signals(self)
                self.widget = self.builder.get_object('table')
                self.label = gtk.Label()
                self.label.set_label("Channel %d" % n)

        def update(self):
                self.device.select_channel(self.n)
                chan, mode, freq, amp, phase = self.device.get_status()
                self.mode = mode
                self.amplitude = amp
                self.frequency = freq
        
        def mode_combo_changed_cb(self, combobox):
                self.device.select_channel(self.n)
                self.device.set_mode(self.mode)
                logging.debug("Setting mode to %s" % self.mode)

        @property
        def mode(self):
                model = self.builder.get_object('mode_store')
                combo = self.builder.get_object('mode_combo')
                iter = model[combo.get_active_iter()]
                return iter[1]

        @mode.setter
        def mode(self, value):
                model = self.builder.get_object('mode_store')
                combo = self.builder.get_object('mode_combo')
                for row in model:
                        if row[1] == value:
                                iter = model.get_iter(row.path)
                                combo.set_active_iter(iter)
                                return

        @property
        def amplitude(self):
                adj = self.builder.get_object('amplitude')
                return adj.get_value()

        @amplitude.setter
        def amplitude(self, value):
                adj = self.builder.get_object('amplitude')
                adj.set_value(value)

        @property
        def frequency(self):
                adj = self.builder.get_object('frequency')
                return adj.get_value()

        @frequency.setter
        def frequency(self, value):
                adj = self.builder.get_object('frequency')
                adj.set_value(value)
                
        def amplitude_value_changed_cb(self, adj):
                self.device.select_channel(self.n)
                self.device.set_amplitude(self.amplitude)
                logging.debug("Setting amplitude to %d." % self.amplitude)

        def frequency_value_changed_cb(self, adj):
                self.device.select_channel(self.n)
                self.device.set_frequency(self.frequency)
                logging.debug("Setting frequency to %d." % self.frequency)

class AotfConfig(object):
        def __init__(self, device):
                self.device = device
                
                self.builder = gtk.Builder()
                self.builder.add_from_file(os.path.join(resource_prefix, 'aotf-ui.glade'))
                self.builder.connect_signals(self)
                self.win = self.builder.get_object('window')
                self.win.connect('destroy', gtk.main_quit)
                
                notebook = self.builder.get_object('notebook')
                self.channels = []
                for ch in range(1,9):
                        chan = AotfChannel(ch, self.device)
                        chan.update()
                        self.channels.append(chan)
                        notebook.append_page(chan.widget, chan.label)

                self.win.show_all()
                
dev = FreqSynth.probe()
a = AotfConfig(dev)
gtk.main()

