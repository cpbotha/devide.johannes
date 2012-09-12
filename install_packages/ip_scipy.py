# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

# this was just an experiment to see how far we could get with
# gohlke's MKL built scipy binaries on Windows. Not far enough
# (and there are licensing issues in any case). Ask me (cpbotha)
# about the details if you're interested, they're in my simplenotes.

import config
from install_package import InstallPackage
import os
import shutil
import sys
import utils

SCIPY_VER = "0.10.1"
SCIPY_BASENAME = "scipy-" + SCIPY_VER
SCIPY_DIRBASE = SCIPY_BASENAME 

if os.name == 'posix':
    SCIPY_ARCHIVE = "%s.tar.gz" % (SCIPY_BASENAME,)
    SCIPY_URL = "http://sourceforge.net/projects/scipy/files/SciPy/%s/%s/download" % (SCIPY_VER, SCIPY_ARCHIVE)

elif os.name == 'nt':
    SCIPY_URL_BASE = "http://graphics.tudelft.nl/~cpbotha/files/devide/johannes_support/gohlke/%s"

    if config.WINARCH == '32bit':
        SCIPY_ARCHIVE = "scipy-%s.win32-py2.7.exe" % (SCIPY_VER,)

    else:
        SCIPY_ARCHIVE = "scipy-%s.win-amd64-py2.7.exe" % (SCIPY_VER,)

    # now construct the full URL
    SCIPY_URL = SCIPY_URL_BASE % (SCIPY_ARCHIVE,)

dependencies = []

class SciPy(InstallPackage):

    def __init__(self):
        self.tbfilename = os.path.join(config.archive_dir, SCIPY_ARCHIVE)
        self.build_dir = os.path.join(config.build_dir, SCIPY_DIRBASE)
        self.inst_dir = os.path.join(config.inst_dir, 'scipy')

    def get(self):
        if os.path.exists(self.tbfilename):
            utils.output("%s already present, not downloading." %
                         (SCIPY_ARCHIVE,))
        else:
            utils.goto_archive()
            utils.urlget(SCIPY_URL, SCIPY_ARCHIVE)

    def unpack(self):
        if os.path.isdir(self.build_dir):
            utils.output("SCIPY source already unpacked, not redoing.")
            return

        utils.output("Unpacking SCIPY source.")
        if os.name == 'posix':
            utils.unpack_build(self.tbfilename)
        else:
            os.mkdir(self.build_dir)
            os.chdir(self.build_dir)
            utils.unpack(self.tbfilename)

    def configure(self):
        pass
    
    def build(self):
        if os.name == 'nt':
            utils.output("Nothing to build (Windows).")

        else:

            # for posix, we have to build the whole shebang.
            os.chdir(self.build_dir)

            # weak test... there are .so files deeper, but they're in platform
            # specific directories
            if os.path.exists('build'):
                utils.output('scipy already built.  Skipping step.')

            else:
                # the build_ext -lg2c is needed on the VLE Centos3 system, else
                # we get lapack related (symbol not found) errors at import scipy
                #ret = os.system('%s setup.py build build_ext -lg2c' % (sys.executable,))
                ret = os.system('%s setup.py build build_ext' % (sys.executable,))
                
                if ret != 0:
                    utils.error('scipy build failed.  Please fix and try again.')

    def install(self):
        # to test for install, just do python -c "import scipy"
        # and test the result (we could just import directly, but that would
        # only work once our invoking python has been stopped and started
        # again)
        os.chdir(config.working_dir) # we need to be elsewhere!
        ret = os.system('%s -c "import scipy"' % (sys.executable,))
        if ret == 0:
            utils.output('scipy already installed.  Skipping step.')

        else:
            utils.output('ImportError test shows that scipy is not '
                         'installed.  Installing...')

            if os.name == 'posix':
                os.chdir(self.build_dir)
                
                ret = os.system('%s setup.py install' % (sys.executable,))
                
                if ret != 0:
                    utils.error('scipy install failed.  Please fix and try again.')

            elif os.name == 'nt':
                # unpack relevant ZIP into Python site-packages dir.
                from distutils import sysconfig
                spd = sysconfig.get_python_lib()

                # copy self.build_dir/PLATLIB/* to python/libs/site-packages/
                # we're not copying SCRIPTS/f2py.py
                pl_dir = os.path.join(self.build_dir, 'PLATLIB')
                utils.copy_glob(os.path.join(pl_dir, '*'), spd)

    def clean_build(self):
        utils.output("Removing build and install directories.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

        from distutils import sysconfig
        scipy_instdir = os.path.join(sysconfig.get_python_lib(), 'scipy')
        
        if os.path.exists(scipy_instdir):
            shutil.rmtree(scipy_instdir)

    def get_installed_version(self):
        import scipy
        return scipy.__version__


        
        

