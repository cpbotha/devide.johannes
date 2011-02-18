# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import utils

BASENAME = "wrapitk"
# use the "maint" branche, trunk is now meant for ITK 4 (in development)
SVN_REPO = \
        "http://wrapitk.googlecode.com/svn/branches/maint"
SVN_REL = 527

dependencies = ['CMake', 'ITK', 'CableSwig', 'SWIG']

class WrapITK(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.archive_dir, BASENAME)
        self.build_dir = os.path.join(config.build_dir, '%s-build' %
                                      (BASENAME,))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)

    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("wrapitk already checked out, skipping step.")

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
            utils.output("wrapitk build already configured.")
            return
        
        if not os.path.exists(self.build_dir):
            os.mkdir(self.build_dir)

        # need unsigned short for itkPyImageFilter
        # with the switches below, I need /bigobj on win64 for the
        # following projects: ITKPyBasePython
        cmake_params = \
                "-DBUILD_TESTING=OFF " \
                "-DCMAKE_BUILD_TYPE=RelWithDebInfo " \
                "-DCMAKE_INSTALL_PREFIX=%s " \
                "-DINSTALL_WRAP_ITK_COMPATIBILITY=NO " \
                "-DITK_DIR=%s " \
                "-DITK_TEST_DRIVER=%s " \
                "-DCableSwig_DIR=%s " \
                "-DSWIG_DIR=%s " \
                "-DSWIG_EXECUTABLE=%s " \
                "-DVTK_DIR=%s " \
                "-DWRAP_ITK_PYTHON=ON " \
                "-DWRAP_complex_double=OFF " \
                "-DWRAP_complex_float=ON " \
                "-DWRAP_covariant_vector_double=OFF " \
                "-DWRAP_covariant_vector_float=ON " \
                "-DWRAP_double=OFF " \
                "-DWRAP_float=ON " \
                "-DWRAP_rgb_unsigned_char=OFF " \
                "-DWRAP_rgb_unsigned_short=ON " \
                "-DWRAP_rgba_unsigned_char=OFF " \
                "-DWRAP_rgba_unsigned_short=OFF " \
                "-DWRAP_signed_char=OFF " \
                "-DWRAP_signed_long=OFF " \
                "-DWRAP_signed_short=ON " \
                "-DWRAP_unsigned_char=OFF " \
                "-DWRAP_unsigned_long=OFF " \
                "-DWRAP_unsigned_short=ON " \
                "-DWRAP_vector_double=OFF " \
                "-DWRAP_vector_float=ON " \
                "-DPYTHON_EXECUTABLE=%s " \
                "-DPYTHON_LIBRARY=%s " \
                "-DPYTHON_INCLUDE_PATH=%s " % \
                (self.inst_dir, config.ITK_DIR,
                 config.ITK_TEST_DRIVER,
                 config.CABLESWIG_DIR,
                 config.SWIG_DIR,
                 config.SWIG_EXECUTABLE, config.VTK_DIR,
                 config.PYTHON_EXECUTABLE,
                 config.PYTHON_LIBRARY,
                 config.PYTHON_INCLUDE_PATH)


        ret = utils.cmake_command(self.build_dir, self.source_dir,
                cmake_params)

        if ret != 0:
            utils.error("Could not configure WrapITK.  Fix and try again.")
        

    def build(self):
        # NB: if you run "make" in wrapitk-build yourself, make sure
        # the johannes python is in the path (by having ran source
        # jpython_setup.sh), as the build process relies on the
        # correct python being available.

        posix_file = os.path.join(self.build_dir, 
                'lib', '_RegistrationPython.so')
        nt_file = os.path.join(self.build_dir, 
                'lib', config.BUILD_TARGET,
                '_RegistrationPython' + config.PYE_EXT)

        if utils.file_exists(posix_file, nt_file):    
            utils.output("WrapITK already built.  Skipping build step.")

        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('WrapITK.sln')

            if ret != 0:
                utils.error("Could not build WrapITK.  Fix and try again.")
        

    def install(self):
        config.WRAPITK_TOPLEVEL = self.inst_dir
        # this dir contains the WrapITK cmake config (WrapITKConfig.cmake)
        config.WRAPITK_DIR = os.path.join(
                self.inst_dir, 'lib', 'InsightToolkit', 'WrapITK')
        # contains all WrapITK shared objects / libraries
        config.WRAPITK_LIB = os.path.join(config.WRAPITK_DIR, 'lib')
        # contains itk.py
        config.WRAPITK_PYTHON = os.path.join(config.WRAPITK_DIR, 'Python')
        # subsequent wrapitk components will need this
        config.WRAPITK_SOURCE_DIR = self.source_dir

        posix_file = os.path.join(
                config.WRAPITK_LIB, '_RegistrationPython.so')
        nt_file = os.path.join(
                config.WRAPITK_LIB, '_RegistrationPython' + config.PYE_EXT)

        if utils.file_exists(posix_file, nt_file):
            utils.output("WrapITK already installed, skipping step.")
        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('WrapITK.sln', install=True)

            if ret != 0:
                utils.error(
                "Could not install WrapITK.  Fix and try again.")
 
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
        import itk
        return itk.GetVersion()


