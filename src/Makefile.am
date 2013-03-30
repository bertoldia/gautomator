## Process this file with automake to produce Makefile.in
## Created by Anjuta


uidir = $(datadir)/gautomator/ui
ui_DATA = gautomator.ui


## The main script
bin_SCRIPTS = gautomator.py

## Directory where .class files will be installed
gautomatordir = $(pythondir)/gautomator


gautomator_PYTHON = \
	gautomator.py


EXTRA_DIST = $(ui_DATA)


# Remove ui directory on uninstall
uninstall-local:

	-rm -r $(uidir)

	-rm -r $(datadir)/gautomator
