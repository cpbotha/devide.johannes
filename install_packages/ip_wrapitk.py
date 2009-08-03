# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import utils

BASENAME = "wrapitk"
SVN_REPO = \
        "http://wrapitk.googlecode.com/svn/tags/0.3.0"
dependencies = ['cmake', 'itk', 'cableswig', 'swig']

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
            ret = os.system("%s co %s %s" % (config.SVN,
                SVN_REPO, BASENAME))
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
            utils.error("Could not configure GDCM.  Fix and try again.")
        

    def build(self):
        raise RuntimeError
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
        # nuke the build dir, the source dir is pristine and there is
        # no installation
        utils.output("Removing build dir.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

    def get_installed_version(self):
        import gdcm
        return gdcm.Version.GetVersion()


