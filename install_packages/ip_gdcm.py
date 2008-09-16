# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import utils

# 2.0.8
GDCM_REL = "4190"

BASENAME = "gdcm"
SVN_REPO = \
        "https://gdcm.svn.sourceforge.net/svnroot/gdcm/branches/gdcm-2-0"
#SVN_REPO = \
#        "https://gdcm.svn.sourceforge.net/svnroot/gdcm/trunk"

SVN_REL = GDCM_REL

PDIR1 = \
"http://visualisation.tudelft.nl/~cpbotha/files/vtk_itk/patches/"

# this patch is for gdcm 2.0.8. ONLY until Mathieu comes with a better
# way to indicate location of Part3.xml.  When you change any of this,
# remember to check devide.spec (it includes Part3.xml) and gdcm_kit
# (it sets up everything so that this file can be found)
XML_PATCH = "gdcm208_gdcmDefs_findxml.diff"
XML_PATCH_URL = PDIR1 + XML_PATCH

dependencies = ['swig', 'vtk']

class GDCM(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.archive_dir, BASENAME)
        self.build_dir = os.path.join(config.build_dir, '%s-build' %
                                      (BASENAME,))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)

        self.xml_patch_name = os.path.join(config.archive_dir,
                XML_PATCH)

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

        if not os.path.exists(self.xml_patch_name):
            utils.goto_archive()
            utils.urlget(XML_PATCH_URL)

            utils.output("Applying XML patch")
            os.chdir(self.source_dir)
            ret = os.system(
                "%s -p0 < %s" % (config.PATCH, self.xml_patch_name))
            if ret != 0:
                utils.error(
                    "Could not apply XML patch.  Fix and try again.")


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

    def get_installed_version(self):
        import gdcm
        return gdcm.Version.GetVersion()


