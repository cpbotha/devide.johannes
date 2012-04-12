# Copyright (c) Francois Malan, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import sys
import utils
from subprocess import call

BASENAME = "particle-system-mm"

#The SciUtah SVN repo contains the standard Sci version excludes Christian's changes and also doesn't build with CMake as is. Included just for reference.
#SVN_REPO = "https://gforge.sci.utah.edu/svn/particle-system-mm"
HG_REPO  = "https://hg.graphics.tudelft.nl/vis/christian/particle-system-mm"

dependencies = ['CMake', 'Teem']

class ParticleSystemMM(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.archive_dir, '%s' %
                                      (BASENAME,))
        self.build_dir = os.path.join(config.build_dir, '%s' %
                                      (BASENAME,))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)
        
    def get(self):    
        if os.path.exists(self.source_dir):
            utils.output("%s already checked out, skipping step." % BASENAME)            
        
        else:
            os.chdir(config.archive_dir)
            ret = os.system("%s clone %s" % (config.HG, HG_REPO))
            if ret != 0:
                utils.error("Could check out %s using HG. Fix and try again." % BASENAME)
                return     
        
    def unpack(self):
        # no unpack step
        pass

    def configure(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'CMakeFiles/cmake.check_cache')):
            utils.output("%s build already configured." % BASENAME)
            return
        
        if not os.path.exists(self.build_dir):
            os.mkdir(self.build_dir)

        cmake_params = "-DCMAKE_BUILD_TYPE=RelWithDebInfo " \
                       "-DCMAKE_INSTALL_PREFIX=%s " \
                       "-DTeem_DIR=%s " \
                        % \
                       (self.inst_dir,config.Teem_DIR)

        ret = utils.cmake_command(self.build_dir, self.source_dir,
                cmake_params)

        if ret != 0:
            utils.error(
                "Could not configure teem.  Fix and try again.")

    def build(self):
        bin_path = os.path.join(self.build_dir,'src','multisurfaces','run-particle-system','optimize-particle-system.dir')

        if utils.file_exists(bin_path, bin_path):    
            utils.output("%s already built.  Skipping build step." % BASENAME)

        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('Project.sln')

            if ret != 0:
                utils.error("Could not build %s.  Fix and try again." % BASENAME)

    def install(self):
        if os.path.exists(
            os.path.join(self.inst_dir, 'bin', 
                'optimize-particle-system' + config.EXE_EXT)):
            utils.output("%s already installed.  Skipping step." % BASENAME)

        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('Project.sln', install=True)

            if ret != 0:
                utils.error(
                    "Could not install %s.  Fix and try again." % BASENAME)
 
    def clean_build(self):
        # nuke the build dir and install dir. The source dir is pristine
        
        utils.output("Removing build dir.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

        utils.output("Removing install dir.")
        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)

    def get_installed_version(self):
        return "NA"

