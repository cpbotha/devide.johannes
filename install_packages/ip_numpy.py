# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import sys
import utils

NUMPY_VER = "1.5.1"
NUMPY_BASENAME = "numpy-" + NUMPY_VER
NUMPY_DIRBASE = NUMPY_BASENAME 

if os.name == 'posix':
    NUMPY_ARCHIVE = "%s.tar.gz" % (NUMPY_BASENAME,)
    NUMPY_URL = "http://sourceforge.net/projects/numpy/files/NumPy/%s/%s/download" % (NUMPY_VER, NUMPY_ARCHIVE)

elif os.name == 'nt':
    NUMPY_URL_BASE = "http://graphics.tudelft.nl/~cpbotha/files/devide/johannes_support/gohlke/%s"

    if config.WINARCH == '32bit':
        NUMPY_ARCHIVE = "%s.win32-py2.7.exe" % (NUMPY_BASENAME,)   

    else:
        NUMPY_ARCHIVE = "%s.win-amd64-py2.7.exe" % (NUMPY_BASENAME,)   

    # now construct the full URL
    NUMPY_URL = NUMPY_URL_BASE % (NUMPY_ARCHIVE,)

dependencies = []

class NumPy(InstallPackage):

    def __init__(self):
        self.tbfilename = os.path.join(config.archive_dir, NUMPY_ARCHIVE)
        self.build_dir = os.path.join(config.build_dir, NUMPY_DIRBASE)
        self.inst_dir = os.path.join(config.inst_dir, 'numpy')

    def get(self):
        if os.path.exists(self.tbfilename):
            utils.output("%s already present, not downloading." %
                         (NUMPY_ARCHIVE,))
        else:
            utils.goto_archive()
            utils.urlget(NUMPY_URL, NUMPY_ARCHIVE)

    def unpack(self):
        if os.path.isdir(self.build_dir):
            utils.output("NUMPY source already unpacked, not redoing.")
            return

        utils.output("Unpacking NUMPY source.")
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
                utils.output('numpy already built.  Skipping step.')

            else:
                # the build_ext -lg2c is needed on the VLE Centos3 system, else
                # we get lapack related (symbol not found) errors at import numpy
                #ret = os.system('%s setup.py build build_ext -lg2c' % (sys.executable,))
                ret = os.system('%s setup.py build build_ext' % (sys.executable,))
                
                if ret != 0:
                    utils.error('numpy build failed.  Please fix and try again.')

    def install(self):
        # to test for install, just do python -c "import numpy"
        # and test the result (we could just import directly, but that would
        # only work once our invoking python has been stopped and started
        # again)
        os.chdir(config.working_dir) # we need to be elsewhere!
        ret = os.system('%s -c "import numpy"' % (sys.executable,))
        if ret == 0:
            utils.output('numpy already installed.  Skipping step.')

        else:
            utils.output('ImportError test shows that numpy is not '
                         'installed.  Installing...')

            if os.name == 'posix':
                os.chdir(self.build_dir)
                
                ret = os.system('%s setup.py install' % (sys.executable,))
                
                if ret != 0:
                    utils.error('numpy install failed.  Please fix and try again.')

            elif os.name == 'nt':
                # unpack relevant ZIP into Python site-packages dir.
                from distutils import sysconfig
                spd = sysconfig.get_python_lib()

                # copy self.build_dir/PLATLIB/numpy to python/libs/site-packages/numpy
                # we're not copying *egg.info or SCRIPTS/f2py.py
                pl_dir = os.path.join(self.build_dir, 'PLATLIB')
                shutil.copytree(os.path.join(pl_dir,'numpy'), os.path.join(spd, 'numpy'), symlinks=True)

    def clean_build(self):
        utils.output("Removing build and install directories.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

        from distutils import sysconfig
        numpy_instdir = os.path.join(sysconfig.get_python_lib(), 'numpy')
        
        if os.path.exists(numpy_instdir):
            shutil.rmtree(numpy_instdir)

    def get_installed_version(self):
        import numpy
        return numpy.__version__


        
        

