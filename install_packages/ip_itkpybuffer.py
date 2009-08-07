# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import sys
import utils

# NB: for this module to build successfully, ITK has to be built with
#     ITK_USE_REVIEW=ON (until the itkFlatStructuringElement moves OUT of the
#     review directory, that is)

BASENAME = "itkPyBuffer"

dependencies = ['cmake', 'itk', 'wrapitk', 'swig']

WIN64 = False
if os.name == 'nt':
    import platform
    a = platform.architecture()[0]
    if a == '64bit':
        WIN64 = True

class itkPyBuffer(InstallPackage):
    
    def __init__(self):
        self.source_dir = '' # will set in get()
        self.build_dir = os.path.join(config.build_dir, '%s-build' %
                                      (BASENAME,))
        #self.inst_dir = os.path.join(config.inst_dir, BASENAME)

    def get(self):
        self.source_dir = os.path.join(
                config.WRAPITK_SOURCE_DIR, 
                'ExternalProjects', 'PyBuffer')
        
        if not os.path.exists(self.source_dir):
            utils.error("itkPyBuffer source not available.  Have you executed "
                        "the WrapITK InstallPackage?")

        else:
            pass

            if False:
                # make sure that ENABLE_TESTING() in the CMakeLists.txt has been
                # deactivated
                repls = [('ENABLE_TESTING\(\)', '')]
                utils.re_sub_filter_file(
                    repls,
                    os.path.join(self.source_dir,'CMakeLists.txt'))

                # and also disable inclusing of Wrapping/Python/Testing dir
                # this will probably change in future versions of itkPyBuffer
                repls = [('SUBDIRS\(Tests\)', '')]
                utils.re_sub_filter_file(
                    repls,
                    os.path.join(self.source_dir,
                                 'Wrapping/Python/CMakeLists.txt'))

    def unpack(self):
        # no unpack step
        pass

    def configure(self):
        if WIN64:
            utils.output(
            'Not building itkPyBuffer on win64 (no numpy).')
            return

        if os.path.exists(
            os.path.join(self.build_dir, 'CMakeFiles/cmake.check_cache')):
            utils.output("itkPyBuffer build already configured.")
            return
        
        if not os.path.exists(self.build_dir):
            os.mkdir(self.build_dir)

        # we need the PATH types for VTK_DIR and for WrapITK_DIR, else
        # these variables are NOT stored.  That's just weird.
        # we also need to pass the same instal prefix as for ITK, so
        # that the external module can be put in the right place.
        cmake_params = "-DBUILD_WRAPPERS=ON " \
                       "-DCMAKE_BUILD_TYPE=RelWithDebInfo " \
                       "-DCMAKE_INSTALL_PREFIX=%s " \
                       "-DITK_DIR=%s " \
                       "-DITK_TEST_DRIVER=%s " \
                       "-DWrapITK_DIR=%s " \
                       "-DSWIG_DIR=%s " \
                       "-DSWIG_EXECUTABLE=%s " \
                       "-DPYTHON_EXECUTABLE=%s " \
                       "-DPYTHON_LIBRARY=%s " \
                       "-DPYTHON_INCLUDE_PATH=%s " \
                        % \
                       (config.WRAPITK_TOPLEVEL,
                        config.ITK_DIR, config.ITK_TEST_DRIVER,
                        config.WRAPITK_DIR,
                        config.SWIG_DIR, config.SWIG_EXECUTABLE,
                        config.PYTHON_EXECUTABLE,
                        config.PYTHON_LIBRARY,
                        config.PYTHON_INCLUDE_PATH)
 
        ret = utils.cmake_command(self.build_dir, self.source_dir,
                cmake_params)

        if ret != 0:
            utils.error(
                "Could not configure itkPyBuffer (P1).  Fix and try again.")


    def build(self):
        if WIN64:
            utils.output(
            'Not building itkPyBuffer on win64 (no numpy).')
            return

        posix_file = os.path.join(
                self.build_dir, 'lib/_BufferConversionPython.so')
        nt_file = os.path.join(self.build_dir, 'lib',
                config.BUILD_TARGET, 
                '_BufferConversionPython' + config.PYE_EXT)

        if utils.file_exists(posix_file, nt_file):
            utils.output("itkPyBuffer already built.  Skipping build step.")

        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('PyBuffer.sln')
            if ret != 0:
                utils.error("Could not build itkPyBuffer.  Fix and try again.")
        

    def install(self):
        if WIN64:
            utils.output(
            'Not building itkPyBuffer on win64 (no numpy).')
            return

        # config.WRAPITK_LIB is something like:
        # /inst/Insight/lib/InsightToolkit/WrapITK/lib
        if os.path.exists(
            os.path.join(config.WRAPITK_LIB, 
                '_BufferConversionPython' + config.PYE_EXT)):
            utils.output("itkPyBuffer already installed.  Skipping step.")

        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('itkPyBuffer.sln', install=True)

            if ret != 0:
                utils.error(
                    "Could not install itkPyBuffer.  Fix and try again.")

 
    def clean_build(self):
        # nuke the build dir, the source dir is pristine and there is
        # no installation
        utils.output("Removing build dir.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

    def get_installed_version(self):
        return "NA"

