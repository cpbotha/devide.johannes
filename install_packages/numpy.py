# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import sys
import utils

NUMPY_TARBALL = "numpy-1.0.4.tar.gz"
NUMPY_URL = "http://surfnet.dl.sourceforge.net/sourceforge/numpy/%s" % \
            (NUMPY_TARBALL,)
NUMPY_DIRBASE = "numpy-1.0.4"

class NumPy(InstallPackage):

    def __init__(self):
        self.tbfilename = os.path.join(config.archive_dir, NUMPY_TARBALL)
        self.build_dir = os.path.join(config.build_dir, NUMPY_DIRBASE)
        self.inst_dir = os.path.join(config.inst_dir, 'numpy')

    def get(self):
        if os.path.exists(self.tbfilename):
            utils.output("%s already present, not downloading." %
                         (NUMPY_TARBALL,))
        else:
            utils.goto_archive()
            utils.urlget(NUMPY_URL)

    def unpack(self):
        if os.path.isdir(self.build_dir):
            utils.output("NUMPY source already unpacked, not redoing.")
        else:
            utils.output("Unpacking NUMPY source.")
            utils.unpack_build(self.tbfilename)

    def configure(self):
        pass
    
    def build(self):
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

            os.chdir(self.build_dir)
            
            ret = os.system('%s setup.py install' % (sys.executable,))
            
            if ret != 0:
                utils.error('numpy install failed.  Please fix and try again.')

    def clean_build(self):
        utils.output("Removing build and install directories.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

        from distutils import sysconfig
        numpy_instdir = os.path.join(sysconfig.get_python_lib(), 'numpy')
        
        if os.path.exists(numpy_instdir):
            shutil.rmtree(numpy_instdir)

        
        

