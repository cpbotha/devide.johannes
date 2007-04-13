DeVIDE - Delft Visualisation and Image processing Environment

This is a completely self-contained source package with which you can
build DeVIDE and all of its prerequisites.  The package contains
'johannes', the build system that makes these source packages and also
knows how to build DeVIDE from scratch.

This software has been customised for the VL-e POC.  In order to build
and install from source, do the following:

1. make sure the following dependencies are installed in your POC
   environment (they aren't by default):
   zlib-devel, bzip2-devel, ncurses-devel, gtk2-devel, libpng-devel
2. ./configure --prefix=/some/directory/devide-abcd.wxyz
3. make
4. make install

Preferably install the pre-built binaries from the POC contrib instead
of building from source.

For more information, you can make use of the following resources:
mailto:c.p.botha@tudelft.nl
http://visualisation.tudelft.nl/Projects/DeVIDE
