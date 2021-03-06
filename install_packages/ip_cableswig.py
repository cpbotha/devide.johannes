# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import utils
import sys

BASENAME = "CableSwig"
# password part of REPO spec
CVS_REPO = ":pserver:anonymous@www.itk.org:/cvsroot/" + BASENAME
CVS_VERSION = "-r ITK-3-20"

dependencies = ['CMake']

class CableSwig(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.archive_dir, BASENAME)
        self.build_dir = os.path.join(config.build_dir, '%s-build' %
                                      (BASENAME,))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)

    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("CableSwig already checked out, skipping step.")

        else:
            os.chdir(config.archive_dir)
            ret = os.system("%s -d %s co %s %s" %
                            (config.CVS, CVS_REPO, CVS_VERSION, BASENAME))
            
            if ret != 0:
                utils.error("Could not CVS checkout.  Fix and try again.")

    def unpack(self):
        pass

    def configure(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'CMakeFiles/cmake.check_cache')):
            utils.output("CableSwig build already configured.")
            return
        
        if not os.path.exists(self.build_dir):
            os.mkdir(self.build_dir)

        cmake_params = "-DBUILD_TESTING=OFF " \
                       "-DCMAKE_BUILD_TYPE=RelWithDebInfo " \
                       "-DCMAKE_INSTALL_PREFIX=%s " \
                      % (self.inst_dir,)

        ret = utils.cmake_command(self.build_dir, self.source_dir,
                cmake_params)

        if ret != 0:
            utils.error("Could not configure CableSwig.  Fix and try again.")

    def build(self):
        posix_file = os.path.join(
                self.build_dir, 'bin', 'cswig')
        nt_file = os.path.join(
                self.build_dir, 'bin', config.BUILD_TARGET,
                'cswig.exe')

        if utils.file_exists(posix_file, nt_file):
            utils.output("CableSwig already built.  Skipping build step.")

        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('CableSwig.sln')
            if ret != 0:
                utils.error("Error building CableSwig.  Fix and try again.")

    def install(self):
        # directory containing cmake config + bin dir
        config.CABLESWIG_DIR = os.path.join(self.inst_dir, \
        'lib/CableSwig')

        if os.path.exists(
            os.path.join(config.CABLESWIG_DIR, 'CableSwigConfig.cmake')):
            utils.output("CableSwig already installed.  Skipping step.")

        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('CableSwig.sln', install=True) 
            if ret != 0:
                utils.error("Could not install CableSwig.  Fix and try again.")

            # when on windows, we have to run CABLESWIG_DIR\gccxml_vcconfig.bat
            if os.name == 'nt':
                os.chdir(os.path.join(
                    config.CABLESWIG_DIR, 'bin'))
                ret = os.system('gccxml_vcconfig.bat')
                if ret != 0:
                    utils.error("Could not run gccxml_vcconfig.bat.")


    def clean_build(self):
        utils.output("Removing build and installation directories.")
        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)

        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)


    def get_installed_version(self):
        return None

        

        
