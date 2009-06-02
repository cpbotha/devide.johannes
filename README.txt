This package contains johannes, a very scary *ix build system for DeVIDE.
Johannes now also Does Windows(tm) in all bits, see WINDOWS.txt for
details on that.  This file deals primarily with *ix.

johannes is copyright 2007-2009 Charl P. Botha <c.p.botha@tudelft.nl>
and is made available under the New BSD License.

Before starting, you need at least the following packages (or
equivalents) on your system:
gcc, g++, cvs, svn, chrpath
bzip2-dev | libbz2-dev, ncurses-dev, gtk2-dev | libgtk2.0-dev,
libxt-dev,
libfreetype-dev, libpng-dev, libzlib-dev (these three for matplotlib)
libatlas-dev (*optional* for faster numpy)
libgl-dev, lubglu-dev

* On Ubuntu / Debian, the following will install all necessary packages:
  sudo apt-get install cvs subversion chrpath g++ gcc\
  libsqlite3-dev libncurses-dev libgtk2.0-dev\
  libxt-dev libfreetype6-dev libpng12-dev libz-dev libbz2-dev\
  libgl1-mesa-dev libglu1-mesa-dev

A. For a NORMAL full build (the default), do the following:
  
  1. sh bootstrap_stage1.sh workingdir
  2. sh bootstrap_stage2.sh workingdir
  3. . workingdir/python_setup_env.sh
  4. python johannes.py -w workingdir

B. To make a fully self-contained source tarball that can be built
  later, do the following (not often used):

  1. sh bootstrap_stage1.sh workingdir
  2. python johannes.py -w workingdir -m get_only
  3. cp -r johannes workingdir

  workingdir can now be tarred up and shipped.  The end-user will:
  1. unpack
  2. sh workingdir/johannes/bootstrap_stage2.sh
  3. . workingdir/python_setup_env.sh
  4. python workingdir/johannes/johannes.py -w workingdir
  
C. To make a fully self-contained vl-e compatible tarball (not often
   used):
  
  1. follow B
  2. cd workingdir/johannes/vle
  3. cp Makefile.in configure README.txt ../..
  4. cd ../../..
  5. mv workingdir devide-xxxx.yyyy.0
  6. tar czvf devide-xxxx.yyyy.0.tar.gz devide-xxxx.yyyy.0

RESULTS
-------

After following strategy A above (or its Windows equivalent as
explained in WINDOWS.txt), you will have three batch files / shell
scripts in your working directory:

* setup_env.sh/cmd: This sets up your environment so that you can work
  with everything you have built.  This has to be run ONCE for every
  console in which you want to make use of the development
  environment.

* devide.sh/cmd: AFTER having run setup_env, use this to invoke DeVIDE
  directly from its build directory.  This is useful if you're doing
  development on the core DeVIDE sources or any of the libraries it
  uses.

* make_devide_package.sh/cmd: AFTER having run setup_env, use this to
  build redistributable, self-contained binaries. These will be
  generated in workingdir/build/devide/installer/distdevide and an
  installer exe or binary tarball will be waiting in
  workingdir/build/devide/installer.  You can send this to your
  friends!
  
Note on Windows
---------------

Due to certain issues on Windows (primarily the difficulty of building
Python extensions automatically if you don't have the exact same
compiler as Python), johannes can NOT build the basic stuff on
Windows.

However, it IS able to build the more complex stuff, such as dcmtk,
itk, vtk and all the other high-level dependencies of DeVIDE.
Please see WINDOWS.txt for more details on what johannes can do for
you on Windows.




