# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import utils

BASENAME = "gdcm"
GIT_REPO = "git://git.code.sf.net/p/gdcm/gdcm "
GIT_TAG = "v2.0.17"

dependencies = ['SWIG', 'VTK']

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
            ret = os.system("git clone %s" % (GIT_REPO,))
            if ret != 0:
                utils.error("Could not clone GDCM repo.  Fix and try again.")

            os.chdir(self.source_dir)
            ret = os.system("git checkout %s" % (GIT_TAG,))
            if ret != 0:
                utils.error("Could not checkout GDCM %s.  Fix and try again." % (GIT_TAG,))


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
                "-DVTK_DIR=%s " \
                "-DPYTHON_EXECUTABLE=%s " \
                "-DPYTHON_LIBRARY=%s " \
                "-DPYTHON_INCLUDE_PATH=%s " % \
                (self.inst_dir, config.SWIG_DIR,
                 config.SWIG_EXECUTABLE, config.VTK_DIR,
                 config.PYTHON_EXECUTABLE,
                 config.PYTHON_LIBRARY,
                 config.PYTHON_INCLUDE_PATH)


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
        if os.name == 'nt':
            config.GDCM_LIB = os.path.join(
                    self.inst_dir, 'bin')
        else:
            config.GDCM_LIB = os.path.join(self.inst_dir, 'lib')

        config.GDCM_PYTHON = os.path.join(self.inst_dir, 'lib')

        test_file = os.path.join(config.GDCM_PYTHON, 'gdcm.py')
        if os.path.exists(test_file):
            utils.output("gdcm already installed, skipping step.")
        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('GDCM.sln', install=True)

            if ret != 0:
                utils.error(
                "Could not install gdcm.  Fix and try again.")
 
    def clean_build(self):
        utils.output("Removing build and installation directories.")
        
        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)
            
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
    
    def clean_install(self):
        utils.output("Removing installation directory.")
        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)
    
    def get_installed_version(self):
        import gdcm
        return gdcm.Version.GetVersion()
    