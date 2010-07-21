from distutils.core import setup

setup(name='aotf-config',
      #version='1.0',
      description="Python interface to Gooch & Housego frequency synthesizer",
      author="Ben Gamari",
      author_email="bgamari@physics.umass.edu",
      url="http://goldnerlab.physics.umass.edu/wiki",
      py_modules=['gooch_housego'],
      scripts=['aotf-ui.py', 'config_aotf.py'],
      data_files=[
              ('share/aotf-config', ['aotf-channel.glade', 'aotf-ui.glade'])
      ],
     )
