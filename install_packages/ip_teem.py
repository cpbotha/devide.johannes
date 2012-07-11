# Copyright (c) Francois Malan, Christian Kehl & Peter Kok, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import sys
import utils

VERSION = "1.10.0"
BASENAME = "teem"

ARCHIVE_BASENAME = "%s-%s" % (BASENAME, VERSION)
ARCHIVE_NAME = "%s-src.tar.gz" % (ARCHIVE_BASENAME,)

URL = "http://prdownloads.sourceforge.net/teem/%s?download" % (ARCHIVE_NAME)

dependencies = ['CMake']

class Teem(InstallPackage):
    
    def __init__(self):
        self.archive_path = os.path.join(
                config.archive_dir, ARCHIVE_NAME)
        self.source_dir = os.path.join(config.build_dir, '%s-%s-src' %
                                      (BASENAME,VERSION))
        self.build_dir = os.path.join(config.build_dir, '%s-%s' %
                                      (BASENAME,VERSION))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)
        config.Teem_DIR = os.path.join(self.inst_dir, 'lib', 'Teem-%s' % VERSION)

    def get(self):
        if os.path.exists(self.archive_path):
            utils.output("%s already present, skipping step." % BASENAME)
            return
        
        utils.goto_archive()
        utils.urlget(URL, ARCHIVE_NAME)
        
    def unpack(self):
        if os.path.exists(self.source_dir):
            utils.output("%s already unpacked. Skipping." % BASENAME)
            return
        
        utils.output("Unpacking %s." % BASENAME)
        utils.unpack_build(self.archive_path)

    def configure(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'CMakeFiles/cmake.check_cache')):
            utils.output("teem build already configured.")
            return
        
        if not os.path.exists(self.build_dir):
            os.mkdir(self.build_dir)

        cmake_params = "-DCMAKE_BUILD_TYPE=RelWithDebInfo " \
                       "-DCMAKE_INSTALL_PREFIX=%s " \
                        % \
                       (self.inst_dir,)

        ret = utils.cmake_command(self.build_dir, self.source_dir,
                cmake_params)

        if ret != 0:
            utils.error(
                "Could not configure teem.  Fix and try again.")

    def build(self):
        bin_path = os.path.join(self.build_dir, 'bin')

        if utils.file_exists(bin_path, bin_path):    
            utils.output("teem already built.  Skipping build step.")

        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('teem.sln')

            if ret != 0:
                utils.error("Could not build teem.  Fix and try again.")

    def install(self):
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
 
    def clean_build(self):
        # nuke the build dir and install dir. The source dir is pristine
        
        utils.output("Removing build dir.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

        utils.output("Removing install dir.")
        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)

    def get_installed_version(self):
        return "version %s" % VERSION

