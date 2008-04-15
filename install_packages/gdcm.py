# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import utils

GDCM_REL = "2947"

BASENAME = "gdcm"
SVN_REPO = \
        "https://gdcm.svn.sourceforge.net/svnroot/gdcm/branches/gdcm-2-0"
SVN_REL = GDCM_REL

dependencies = ['swig', 'vtk']

class GDCM(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.archive_dir, BASENAME)
        self.build_dir = os.path.join(config.build_dir, '%s-build' %
                                      (BASENAME,))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)

    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("gdcm already checked out, skipping step.")

        else:
            os.chdir(config.archive_dir)
            # checkout trunk into directory vtktudoss
            ret = os.system("%s co %s %s -r%s" % (config.SVN,
                SVN_REPO, BASENAME, SVN_REL))
            if ret != 0:
                utils.error("Could not SVN checkout.  Fix and try again.")

    def unpack(self):
        # no unpack step
        pass

    def configure(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'CMakeFiles/cmake.check_cache')):
            utils.output("gdcm build already configured.")
            return
        
        if not os.path.exists(self.build_dir):
            os.mkdir(self.build_dir)

        cmake_params = \
                "-DGDCM_BUILD_APPLICATIONS=OFF " \
                "-DGDCM_BUILD_EXAMPLES=OFF " \
                "-DGDCM_BUILD_SHARED_LIBS=ON " \
                "-DGDCM_BUILD_TESTING=OFF " \
                "-DGDCM_USE_ITK=OFF " \
                "-DGDCM_USE_VTK=ON " \
                "-DGDCM_USE_WXWIDGETS=OFF " \
                "-DGDCM_WRAP_JAVA=OFF " \
                "-DGDCM_WRAP_PHP=OFF " \
                "-DGDCM_WRAP_PYTHON=ON " \
                "-DCMAKE_BUILD_TYPE=RelWithDebInfo " \
                "-DCMAKE_INSTALL_PREFIX=%s " \
                "-DSWIG_DIR=%s " \
                "-DSWIG_EXECUTABLE=%s " \
                "-DVTK_DIR=%s " % \
                (self.inst_dir, config.SWIG_DIR,
                        config.SWIG_EXECUTABLE, config.VTK_DIR)

        ret = utils.cmake_command(self.build_dir, self.source_dir,
                cmake_params)

        if ret != 0:
            utils.error("Could not configure GDCM.  Fix and try again.")
        

    def build(self):
        posix_file = os.path.join(self.build_dir, 
                'bin/libvtkgdcmPython.so')
        nt_file = os.path.join(self.build_dir, 'bin',
                config.BUILD_TARGET, 'vtkgdcmPythonD.dll')

        if utils.file_exists(posix_file, nt_file):    
            utils.output("GDCM already built.  Skipping build step.")

        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('GDCM.sln')

            if ret != 0:
                utils.error("Could not build GDCM.  Fix and try again.")
        

    def install(self):
        config.GDCM_LIB = os.path.join(self.build_dir, 'bin')
        if os.name == 'nt':
            config.GDCM_LIB = os.path.join(
                    config.GDCM_LIB, config.BUILD_TARGET)

        config.GDCM_PYTHON = os.path.join(self.build_dir, 'bin')
 
    def clean_build(self):
        # nuke the build dir, the source dir is pristine and there is
        # no installation
        utils.output("Removing build dir.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

