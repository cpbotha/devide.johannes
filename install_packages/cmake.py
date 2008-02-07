# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import utils

CMAKE_TARBALL = "cmake-2.4.8.tar.gz"
CMAKE_URL = "http://www.cmake.org/files/v2.4/%s" % (CMAKE_TARBALL,)
CMAKE_DIRBASE = "cmake-2.4.8"

class CMake(InstallPackage):
    
    def __init__(self):
        self.tbfilename = os.path.join(config.archive_dir, CMAKE_TARBALL)
        self.build_dir = os.path.join(config.build_dir, CMAKE_DIRBASE)
        self.inst_dir = os.path.join(config.inst_dir, 'cmake')

    def get(self):
        if os.path.exists(self.tbfilename):
            utils.output("%s already present, not downloading." %
                         (CMAKE_TARBALL,))
        else:
            utils.goto_archive()
            utils.urlget(CMAKE_URL)

    def unpack(self):
        if os.path.isdir(self.build_dir):
            utils.output("CMAKE source already unpacked, not redoing.")
        else:
            utils.output("Unpacking CMAKE source.")
            utils.unpack_build(self.tbfilename)

    def configure(self):
        os.chdir(self.build_dir)
        
        if os.path.exists("Bootstrap.cmk/cmake_bootstrap.log"):
            utils.output("CMAKE already configured.  Not redoing.")
        else:
            ret = os.system('./bootstrap --prefix=%s' % (self.inst_dir,))
            if ret != 0:
                utils.error('Could not configure cmake.  Fix and try again.')

    def build(self):
        os.chdir(self.build_dir)
        if os.path.exists("bin/cmake"):
            utils.output("CMAKE already built. Skipping.")

        else:
            ret = os.system('make')
            if ret != 0:
                utils.error('Could not build cmake.  Fix and try again.')

    def install(self):
        cmake_binpath = os.path.join(self.inst_dir, 'bin/cmake')
        if os.path.exists(cmake_binpath):
            utils.output("CMAKE already installed. Skipping.")

        else:
            ret = os.system('make install')
            if ret != 0:
                utils.error('Could not install cmake.  Fix and try again.')

        # either way, we have to register our binary path with config
        config.CMAKE_BINPATH = cmake_binpath

    def clean_build(self):
        utils.output("Removing build and install directories.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)

        
        
