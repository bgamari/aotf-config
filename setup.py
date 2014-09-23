#!/usr/bin/python

from distutils.core import setup

setup(name='aotf-config',
      #version='1.0',
      description="Python interface to Gooch & Housego frequency synthesizer",
      author="Ben Gamari",
      author_email="bgamari@physics.umass.edu",
      url="http://goldnerlab.physics.umass.edu/wiki",
      py_modules=['gooch_housego', 'usbtmc'],
      scripts=['aotf-ui', 'aotf-config', 'aotf-freq-scan', 'aotf-power-scan'],
      data_files=[
              ('share/aotf-config', ['aotf-channel.glade', 'aotf-ui.glade']),
              ('/etc/udev/rules.d', ['thorlabs-pm100.rules']),
              ('/etc/udev/rules.d', ['99-gooch-housego-aotf.rules']),
              ('share/icons', ['aotf-ui.svg']),
              ('share/applications', ['aotf-ui.desktop']),
      ],
     )
