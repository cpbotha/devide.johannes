# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import sys
import utils

EZ_BASENAME = "ez_setup.py"
EZ_SETUP_URL = "http://peak.telecommunity.com/dist/" + EZ_BASENAME
PIP_BASENAME = "get-pip.py"
PIP_URL = "https://raw.github.com/pypa/pip/master/contrib/" + PIP_BASENAME

dependencies = []

class pip(InstallPackage):

    def __init__(self):
        self.ez_afilename = os.path.join(
            config.archive_dir, EZ_BASENAME)
        self.pip_afilename = os.path.join(
            config.archive_dir, PIP_BASENAME)

    def get(self):
        if os.path.exists(self.ez_afilename):
            utils.output("%s already present, not downloading." %
                         (EZ_BASENAME,))

        else:
            utils.goto_archive()
            utils.urlget(EZ_SETUP_URL)
            
        if os.path.exists(self.pip_afilename):
            utils.output("%s already present, not downloading." %
                         (PIP_BASENAME,))

        else:
            utils.goto_archive()
            utils.urlget(PIP_URL)

    def unpack(self):
        pass

    def configure(self):
        pass
    
    def build(self):
        pass

    def install(self):
        # first ez_install ############################################
        os.chdir(config.working_dir) # we need to be elsewhere!
        ret = os.system('%s -c "import setuptools"' % (sys.executable,))
        if ret == 0:
            utils.output('setuptools already installed.  Skipping step.')

        else:
            utils.output('ImportError test shows that setuptools is not '
                         'installed.  Installing...')

            os.chdir(config.archive_dir)
            ret = os.system('%s %s' %
                    (config.PYTHON_EXECUTABLE, EZ_BASENAME))
                    
            if ret != 0:
                utils.error('Error during setuptools install.')

        # then pip # ##############################################

        os.chdir(config.working_dir) # we need to be elsewhere!
        ret = os.system('%s -c "import pip"' % (sys.executable,))
        if ret == 0:
            utils.output('pip already installed.  Skipping step.')

        else:
            utils.output('ImportError test shows that pip is not '
                         'installed.  Installing...')

            os.chdir(config.archive_dir)
            ret = os.system('%s %s' %
                    (config.PYTHON_EXECUTABLE, PIP_BASENAME))
            if ret != 0:
                utils.error('Error during pip install.')

    def clean_build(self):
        pass
        
    def get_installed_version(self):
        return "unknown"

        
        

