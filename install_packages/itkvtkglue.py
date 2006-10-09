import config
from install_package import InstallPackage
import os
import shutil
import utils

BASENAME = "ItkVtkGlue"
SVN_REPO = "https://stockholm.twi.tudelft.nl/svn/tudvis/trunk/" + BASENAME

class ItkVtkGlue(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.WRAPITK_SOURCE_DIR,,
                                       'ExternalProjects/ItkVtkGlue')
        self.build_dir = os.path.join(config.build_dir, '%s-build' %
                                      (BASENAME,))
        #self.inst_dir = os.path.join(config.inst_dir, BASENAME)

    def get(self):
        if not os.path.exists(self.source_dir):
            utils.error("ItkVtkGlue source not available.  Have you executed "
                        "the ITK InstallPackage?")

    def unpack(self):
        # no unpack step
        pass

    def configure(self):

        return
        
        if os.path.exists(
            os.path.join(self.build_dir, 'CMakeFiles/cmake.check_cache')):
            utils.output("vtktud build already configured.")
            return
        
        if not os.path.exists(self.build_dir):
            os.mkdir(self.build_dir)

        os.chdir(self.build_dir)
        cmake_params = "-DBUILD_SHARED_LIBS=ON " \
                       "-DBUILD_TESTING=OFF " \
                       "-DCMAKE_BUILD_TYPE=RelWithDebInfo " \
                       "-DCMAKE_INSTALL_PREFIX=%s " \
                       "-DVTK_DIR=%s" % (self.inst_dir, config.VTK_DIR)

        ret = os.system("%s %s %s" %
                        (config.CMAKE, cmake_params, self.source_dir))

        if ret != 0:
            utils.error("Could not configure vtktud.  Fix and try again.")
        

    def build(self):
        return
        
        if os.path.exists(
            os.path.join(self.build_dir, 'bin/libvtktudImagingPython.so')):

            utils.output("vtktud already built.  Skipping build step.")

        else:
            os.chdir(self.build_dir)
            ret = os.system("%s" % (config.MAKE,))
            if ret != 0:
                utils.error("Could not build vtktud.  Fix and try again.")
        

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
