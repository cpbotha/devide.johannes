This package contains johannes, a very scary build system for DeVIDE.

You need at least the following packages (or equivalents) on your system:
gcc, g++, cvs, svn, chrpath
bzip2-dev | libbz2-dev, ncurses-dev, gtk2-dev | libgtk2.0-dev,
libfreetype-dev, libpng-dev, libzlib-dev (these three for matplotlib)
libatlas-dev (*optional* for faster numpy)

A. For a normal full build, do the following:
  
  1. sh bootstrap_stage1.sh workingdir
  2. sh bootstrap_stage2.sh workingdir
  3. . workingdir/python_setup_env.sh
  4. python johannes.py -w workingdir

B. To make a fully self-contained source tarball that can be built
  later, do the following:

  1. sh bootstrap_stage1.sh workingdir
  2. python johannes.py -w workingdir -m get_only
  3. cp -r johannes workingdir

  workingdir can now be tarred up and shipped.  The end-user will:
  1. unpack
  2. sh workingdir/johannes/bootstrap_stage2.sh
  3. . workingdir/python_setup_env.sh
  4. python workingdir/johannes/johannes.py -w workingdir
  
C. To make a fully self-contained vl-e compatible tarball:
  
  1. follow B
  2. cd workingdir/johannes/vle
  3. cp Makefile.in configure README.txt ../..
  4. cd ../../..
  5. mv workingdir devide-xxxx.yyyy.0
  6. tar czvf devide-xxxx.yyyy.0.tar.gz devide-xxxx.yyyy.0
  

-- 
March 2007
Charl P. Botha <c.p.botha@tudelft.nl>
