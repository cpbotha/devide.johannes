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

BASENAME = "VispackMorphsmooth"
VERSION = "1.5"

ARCHIVE_BASENAME = "%s_%s" % (BASENAME, VERSION)
ARCHIVE_NAME = "%s.zip" % (ARCHIVE_BASENAME,)

URL = "http://www.sci.utah.edu/releases/vispack_v1.5/%s" % (ARCHIVE_NAME)
SVN_REPO = "https://gforge.sci.utah.edu/svn/vispack"

dependencies = ['CMake']

# this patch does two things:
# 1. forces building vispack in BIOMESH3D mode (without LAPACK). This enables
#    it to build on Win32. We only need the morphsmooth app as output anyway.
# 2. renames the project from vispack to vispack_morphsmooth to avoid confusion with the
#    original
MORPHSMOOTH_PATCH = "vispack_morphsmooth_only.diff"

class VispackMorphsmooth(InstallPackage):    
    def __init__(self):
        self.archive_path = os.path.join(
                config.archive_dir, ARCHIVE_NAME)
        self.source_dir = os.path.join(config.archive_dir, BASENAME)
        self.build_dir = os.path.join(config.build_dir, BASENAME)
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)
        self.morphsmooth_patch_src = os.path.join(config.patches_dir, MORPHSMOOTH_PATCH)
        self.morphsmooth_patch_dst = os.path.join(self.source_dir, MORPHSMOOTH_PATCH)                

    def get(self):    
        if os.path.exists(self.source_dir):
            utils.output("%s already checked out, skipping step." % BASENAME)            
        
        else:
            os.chdir(config.archive_dir)
            ret = call("%s co %s %s" % \
                (config.SVN, SVN_REPO, BASENAME), shell=True)
            if ret != 0:
                utils.error("Could not SVN checkout. Fix and try again.")
                return

            if not os.path.exists(self.morphsmooth_patch_dst):
                utils.output("Applying vispack_morphsmooth_only patch")
                # we do this copy so we can see if the patch has been done yet or not
                shutil.copyfile(self.morphsmooth_patch_src, self.morphsmooth_patch_dst)                        
                os.chdir(self.source_dir)
                # we have to strip the leading directory names (included by diff) from the patch filenames, hence the -p1
                ret = os.system(
                    "%s -p1 < %s" % (config.PATCH, MORPHSMOOTH_PATCH))

            if ret != 0:
                utils.error(
                    "Could not apply vispack_morphsmooth_only patch.  Fix and try again.")
        
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
                "Could not configure %s.  Fix and try again." % BASENAME)

    def build(self):
        bin_path = os.path.join(self.build_dir, 'apps', 'tighten', 'RelWithDebInfo')

        if utils.file_exists(bin_path, bin_path):    
            utils.output("%s already built.  Skipping build step." % BASENAME)

        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('VispackMorphsmooth.sln')

            if ret != 0:
                utils.error("Could not build %s.  Fix and try again." % BASENAME)

    def install(self):
        '''
        if os.path.exists(
            os.path.join(self.inst_dir, 'bin', 
                'unu' + config.EXE_EXT)):
            utils.output("teem already installed.  Skipping step.")

        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('teem.sln', install=True)

            if ret != 0:
                utils.error(
                    "Could not install teem.  Fix and try again.")
        '''
 
    def clean_build(self):
        '''
        # nuke the build dir and install dir. The source dir is pristine
        
        utils.output("Removing build dir.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

        utils.output("Removing install dir.")
        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)
        '''

    def get_installed_version(self):
        return "version %s" % VERSION

