# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import utils

BASENAME = "vtkdevide"
SVN_REPO = "http://devide.googlecode.com/svn/trunk/" + BASENAME
# this should be the same release as johannes and the rest of devide
SVN_REL = config.DEVIDE_REL

dependencies = ['vtk']

class VTKDEVIDE(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.archive_dir, BASENAME)
        self.build_dir = os.path.join(config.build_dir, '%s-build' %
                                      (BASENAME,))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)

    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("vtkdevide already checked out, skipping step.")

        else:
            os.chdir(config.archive_dir)
            ret = os.system("%s co %s -r%s" % (config.SVN, SVN_REPO, SVN_REL))
            if ret != 0:
                utils.error("Could not SVN checkout.  Fix and try again.")

    def unpack(self):
        # no unpack step
        pass

    def configure(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'CMakeFiles/cmake.check_cache')):
            utils.output("vtkdevide build already configured.")
            return
        
        if not os.path.exists(self.build_dir):
            os.mkdir(self.build_dir)

        cmake_params = "-DBUILD_SHARED_LIBS=ON " \
                       "-DBUILD_TESTING=OFF " \
                       "-DCMAKE_BUILD_TYPE=RelWithDebInfo " \
                       "-DCMAKE_INSTALL_PREFIX=%s " \
                       "-DVTK_DIR=%s " \
                       "-DDCMTK_INCLUDE_PATH=%s " \
                       "-DDCMTK_LIB_PATH=%s" % \
                       (self.inst_dir, config.VTK_DIR,
                        config.DCMTK_INCLUDE, config.DCMTK_LIB)

        ret = utils.cmake_command(self.build_dir, self.source_dir,
                cmake_params)

        if ret != 0:
            utils.error("Could not configure vtkdevide.  Fix and try again.")
        

    def build(self):
        posix_file = os.path.join(self.build_dir, 
                'bin/libvtkdevideExternalPython.so')
        nt_file = os.path.join(self.build_dir, 'bin',
                config.BUILD_TARGET, 
                'vtkdevideExternalPython' + config.PYE_EXT)

        if utils.file_exists(posix_file, nt_file):    
            utils.output("vtkdevide already built.  Skipping build step.")

        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('VTKDEVIDE.sln')
            if ret != 0:
                utils.error("Could not build vtkdevide.  Fix and try again.")
        

    def install(self):
        config.VTKDEVIDE_PYTHON = os.path.join(
            self.inst_dir, 'lib')

        config.VTKDEVIDE_LIB = os.path.join(self.inst_dir, 'lib')
        if os.name == 'nt':
            config.VTKDEVIDE_LIB = os.path.join(
                    config.VTKDEVIDE_LIB, config.BUILD_TARGET)

        test_file = os.path.join(config.VTKDEVIDE_LIB, 'vtkdevide.py')
        if os.path.exists(test_file):
            utils.output("vtkdevide already installed, skipping step.")
        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('VTKDEVIDE.sln', install=True)

            if ret != 0:
                utils.error(
                "Could not install vtkdevide.  Fix and try again.")
 

    def clean_build(self):
        # nuke the build dir, the source dir is pristine and there is
        # no installation
        utils.output("Removing build dir.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

    def get_installed_version(self):
        return None
       
