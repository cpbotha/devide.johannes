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
SVN_REPO = "https://stockholm.twi.tudelft.nl/svn/tudvis/trunk/" + BASENAME

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

        os.chdir(self.build_dir)
        cmake_params = "-DBUILD_WRAPPERS=ON " \
                       "-DCMAKE_BUILD_TYPE=RelWithDebInfo " \
                       "-DITK_DIR=%s " \
                       "-DVTK_DIR=%s " \
                       "-DWrapITK_DIR=%s " \
                       "-DPYTHON_INCLUDE_PATH=%s " \
                       "-DPYTHON_LIBRARY=%s " \
                       "-DPYTHON_EXECUTABLE=%s " \
                       % \
                       (config.ITK_DIR, config.VTK_DIR, config.WRAPITK_DIR,
                        config.python_include_path, config.python_library,
                        sys.executable)

        ret = os.system("%s %s %s" %
                        (config.CMAKE, cmake_params, self.source_dir))

        if ret != 0:
            utils.error("Could not configure ItkVtkGlue.  Fix and try again.")
        

    def build(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'bin/libvtktudImagingPython.so')):

            utils.output("ItkVtkGlue already built.  Skipping build step.")

        else:
            os.chdir(self.build_dir)
            ret = os.system("%s" % (config.MAKE,))
            if ret != 0:
                utils.error("Could not build ItkVtkGlue.  Fix and try again.")
        

    def install(self):
        return
        config.VTKTUD_LIB = os.path.join(self.build_dir, 'bin')
        config.VTKTUD_PYTHON = os.path.join(
            self.source_dir, 'Wrapping/Python')
 
    def clean_build(self):
        # nuke the build dir, the source dir is pristine and there is
        # no installation
        utils.output("Removing build dir.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
