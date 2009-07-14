# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import utils

CMAKE_VER = "2.6.4"


if os.name == 'posix':
    CMAKE_ARCHIVE = "cmake-%s.tar.gz" % (CMAKE_VER,)
    CMAKE_DIRBASE = "cmake-%s" % (CMAKE_VER,)
elif os.name == 'nt':
    CMAKE_DIRBASE = "cmake-%s-win32-x86" % (CMAKE_VER,)
    CMAKE_ARCHIVE = "%s.zip" % (CMAKE_DIRBASE,)

CMAKE_URL = "http://www.cmake.org/files/v2.6/%s" % (CMAKE_ARCHIVE,)

dependencies = []

class CMake(InstallPackage):
    
    def __init__(self):
        self.afilename = os.path.join(config.archive_dir, CMAKE_ARCHIVE)
        self.build_dir = os.path.join(config.build_dir, CMAKE_DIRBASE)
        self.inst_dir = os.path.join(config.inst_dir, 'cmake')

    def get(self):
        if os.path.exists(self.afilename):
            utils.output("%s already present, not downloading." %
                         (CMAKE_ARCHIVE,))
        else:
            utils.goto_archive()
            utils.urlget(CMAKE_URL)

    def unpack(self):
        if os.name == 'nt':
            utils.output('Skipping unpack (WINDOWS).')
            return

        if os.path.isdir(self.build_dir):
            utils.output("CMAKE source already unpacked, not redoing.")
        else:
            utils.output("Unpacking CMAKE source.")
            utils.unpack_build(self.afilename)

    def configure(self):
        if os.name == 'nt':
            utils.output('Skipping configure (WINDOWS).')
            return

        os.chdir(self.build_dir)
        
        if os.path.exists("Bootstrap.cmk/cmake_bootstrap.log"):
            utils.output("CMAKE already configured.  Not redoing.")
        else:
            ret = os.system('./bootstrap --prefix=%s' % (self.inst_dir,))
            if ret != 0:
                utils.error('Could not configure cmake.  Fix and try again.')

    def build(self):
        if os.name == 'nt':
            utils.output('Skipping build (WINDOWS).')
            return

        os.chdir(self.build_dir)
        if os.path.exists("bin/cmake"):
            utils.output("CMAKE already built. Skipping.")

        else:
            ret = os.system('make')
            if ret != 0:
                utils.error('Could not build cmake.  Fix and try again.')

    def install_nt(self):
        config.CMAKE_BINPATH = os.path.join(
                self.inst_dir, 'bin', 'cmake.exe')


        utils.goto_inst()
        if os.path.exists('cmake'):
            utils.output('CMAKE already installed, Skipping.')
            return

        # this will unpack into inst/cmake-VER-win32-x86/bin etc
        utils.unpack(self.afilename)
        # so we rename it to plain 'cmake'
        os.rename(CMAKE_DIRBASE, 'cmake')

    def install_posix(self):
        cmake_binpath = os.path.join(self.inst_dir, 'bin/cmake')
        if os.path.exists(cmake_binpath):
            utils.output("CMAKE already installed. Skipping.")

        else:
            ret = os.system('make install')
            if ret != 0:
                utils.error('Could not install cmake.  Fix and try again.')

        # either way, we have to register our binary path with config
        config.CMAKE_BINPATH = cmake_binpath

    def install(self):
        if os.name == 'posix':
            self.install_posix()

        elif os.name == 'nt':
            self.install_nt()

    def clean_build(self):
        utils.output("Removing build and install directories.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)

    def get_installed_version(self):
        version = None

        local_cmake_path = os.path.join(self.inst_dir, 'bin', 'cmake')
        if os.path.exists(local_cmake_path):
            status,output = utils.get_status_output('%s --version' %
                    (local_cmake_path,))

            if status is None:
                return '%s (local)' % (output.strip(),)

        status,output = utils.get_status_output('cmake --version')
        if status is None:
            return '%s (system)' % (output.strip(),)

        return 'Not found.'

            


        
        
