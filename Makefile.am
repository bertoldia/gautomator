## Process this file with automake to produce Makefile.in
## Created by Anjuta

SUBDIRS = src 

gautomatordocdir = ${prefix}/doc/gautomator
gautomatordoc_DATA = \
	README\
	COPYING\
	AUTHORS\
	ChangeLog\
	INSTALL\
	NEWS


EXTRA_DIST = $(gautomatordoc_DATA)


# Remove doc directory on uninstall
uninstall-local:
	-rm -r $(gautomatordocdir)
