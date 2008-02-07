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

BASENAME = "ItkVtkGlue"

class ItkVtkGlue(InstallPackage):
    
    def __init__(self):
        self.source_dir = '' # will set in get()
        self.build_dir = os.path.join(config.build_dir, '%s-build' %
                                      (BASENAME,))
        #self.inst_dir = os.path.join(config.inst_dir, BASENAME)

    def get(self):
        self.source_dir = os.path.join(config.WRAPITK_SOURCE_DIR,
                                       'ExternalProjects/ItkVtkGlue')
        
        if not os.path.exists(self.source_dir):
            utils.error("ItkVtkGlue source not available.  Have you executed "
                        "the ITK InstallPackage?")

        else:
            # make sure that ENABLE_TESTING() in the CMakeLists.txt has been
            # deactivated
            repls = [('ENABLE_TESTING\(\)', '')]
            utils.re_sub_filter_file(
                repls,
                os.path.join(self.source_dir,'CMakeLists.txt'))

            # and also disable inclusing of Wrapping/Python/Testing dir
            # this will probably change in future versions of ItkVtkGlue
            repls = [('SUBDIRS\(Tests\)', '')]
            utils.re_sub_filter_file(
                repls,
                os.path.join(self.source_dir,
                             'Wrapping/Python/CMakeLists.txt'))

    def unpack(self):
        # no unpack step
        pass

    def configure(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'CMakeFiles/cmake.check_cache')):
            utils.output("itkvtkglue build already configured.")
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
                       "-DVTK_DIR:PATH=%s " \
                       "-DITK_DIR=%s " \
                       "-DWrapITK_DIR:PATH=%s " \
                       "-DPYTHON_EXECUTABLE=%s " \
                       % \
                       (config.ITK_INSTALL_PREFIX,
                        config.VTK_DIR, config.ITK_DIR, config.WRAPITK_DIR,
                        sys.executable)

        ret = utils.cmake_command(self.build_dir, self.source_dir,
                cmake_params)

        if ret != 0:
            utils.error(
                "Could not configure ItkVtkGlue (P1).  Fix and try again.")


    def build(self):
        posix_file = os.path.join(self.build_dir, 'lib/_ItkVtkGluePython.so')
        nt_file = os.path.join(self.build_dir, 'lib',
                config.BUILD_TARGET, 
                '_ItkVtkGluePython' + config.PYE_EXT)

        if utils.file_exists(posix_file, nt_file):
            utils.output("ItkVtkGlue already built.  Skipping build step.")

        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('ItkVtkGlue.sln')
            if ret != 0:
                utils.error("Could not build ItkVtkGlue.  Fix and try again.")
        

    def install(self):
        # config.WRAPITK_LIB is something like:
        # /inst/Insight/lib/InsightToolkit/WrapITK/lib
        if os.path.exists(
            os.path.join(config.WRAPITK_LIB, 
                '_ItkVtkGluePython' + config.PYE_EXT)):
            utils.output("ItkVtkGlue already installed.  Skipping step.")

        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('ItkVtkGlue.sln', install=True)

            if ret != 0:
                utils.error(
                    "Could not install ItkVtkGlue.  Fix and try again.")

 
    def clean_build(self):
        # nuke the build dir, the source dir is pristine and there is
        # no installation
        utils.output("Removing build dir.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
