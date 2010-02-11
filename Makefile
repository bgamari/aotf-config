PREFIX=/usr

all :

install :
	cp gooch_housego.py ${PREFIX}/lib/pymodules/python2.6
	cp config_aotf.py aotf-ui.py ${PREFIX}/bin
	mkdir -p ${PREFIX}/share/aotf-config
	cp aotf-channel.glade aotf-ui.glade ${PREFIX}/share/aotf-config

