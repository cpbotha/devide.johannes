# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import sys
import utils

URL_BASE = "http://ipython.scipy.org/dist/0.10/"

IPY_BASENAME = "ipython-0.10"
IPY_ARCHIVE = IPY_BASENAME + '.tar.gz'
IPY_URL = URL_BASE + IPY_ARCHIVE

PYRL_BASENAME = "pyreadline-1.5"
PYRL_ARCHIVE = PYRL_BASENAME + '.tar.gz'
PYRL_URL = URL_BASE + PYRL_ARCHIVE

dependencies = []

class IPython(InstallPackage):

    def __init__(self):
        self.ipy_afilename = os.path.join(
                config.archive_dir, IPY_ARCHIVE)
        self.pyrl_afilename = os.path.join(
                config.archive_dir, PYRL_ARCHIVE)

        self.ipy_build_dir = os.path.join(
                config.build_dir, IPY_BASENAME)
        self.pyrl_build_dir = os.path.join(
                config.build_dir, PYRL_BASENAME)

    def get(self):
        if os.path.exists(self.ipy_afilename):
            utils.output("%s already present, not downloading." %
                         (IPY_ARCHIVE,))

        else:
            utils.goto_archive()
            utils.urlget(IPY_URL)

        if os.name == 'nt':
            if os.path.exists(self.pyrl_afilename):
                utils.output("%s already present, not downloading." %\
                        (PYRL_ARCHIVE,))
            else:
                utils.goto_archive()
                utils.urlget(PYRL_URL)

    def unpack(self):
        if os.path.isdir(self.ipy_build_dir):
            utils.output('ipython source already unpacked.')
        else:
            utils.output('unpacking ipython source')
            utils.unpack_build(self.ipy_afilename)

        if os.name == 'nt':
            if os.path.isdir(self.pyrl_build_dir):
                utils.output('pyreadline already unpacked.')
            else:
                utils.output('unpacking pyreadline source.')
                utils.unpack_build(self.pyrl_afilename)

    def configure(self):
        pass
    
    def build(self):
        pass

    def install(self):
        # first pyreadline ############################################
        os.chdir(config.working_dir) # we need to be elsewhere!
        ret = os.system('%s -c "import readline"' % (sys.executable,))
        if ret == 0:
            utils.output('PyReadline already installed.  Skipping step.')

        else:
            utils.output('ImportError test shows that PyReadline is not '
                         'installed.  Installing...')

            os.chdir(self.pyrl_build_dir)
            ret = os.system('%s setup.py install' %
                    (config.PYTHON_EXECUTABLE,))
            if ret != 0:
                utils.error('Error during PyReadline install.')

        # then ipython # ##############################################

        # to test for install, just do python -c "import IPython"
        # and test the result (we could just import directly, but that would
        # only work once our invoking python has been stopped and started
        # again)
        os.chdir(config.working_dir) # we need to be elsewhere!
        ret = os.system('%s -c "import IPython"' % (sys.executable,))
        if ret == 0:
            utils.output('IPython already installed.  Skipping step.')

        else:
            utils.output('ImportError test shows that IPython is not '
                         'installed.  Installing...')

            os.chdir(self.ipy_build_dir)
            ret = os.system('%s setup.py install' %
                    (config.PYTHON_EXECUTABLE,))
            if ret != 0:
                utils.error('Error during ipython install.')

    def clean_build(self):
        utils.output("Removing build and install directories.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

        from distutils import sysconfig
        numpy_instdir = os.path.join(sysconfig.get_python_lib(), 'numpy')
        
        if os.path.exists(numpy_instdir):
            shutil.rmtree(numpy_instdir)

    def get_installed_version(self):
        return "unknown"

        
        

