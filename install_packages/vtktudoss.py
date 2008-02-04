import config
from install_package import InstallPackage
import os
import shutil
import utils

BASENAME = "vtktudoss"
SVN_REPO = "http://vtktudoss.googlecode.com/svn/trunk/"
SVN_REL = config.VTKTUDOSS_REL

class VTKTUDOSS(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.archive_dir, BASENAME)
        self.build_dir = os.path.join(config.build_dir, '%s-build' %
                                      (BASENAME,))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)

    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("vtktudoss already checked out, skipping step.")

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
            utils.output("vtktudoss build already configured.")
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
            utils.error("Could not configure vtktudoss.  Fix and try again.")
        

    def build(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'bin/libvtktudossGraphicsPython.so')):

            utils.output("vtktudoss already built.  Skipping build step.")

        else:
            os.chdir(self.build_dir)
            ret = os.system("%s" % (config.MAKE,))
            if ret != 0:
                utils.error("Could not build vtktudoss.  Fix and try again.")
        

    def install(self):
        config.VTKTUDOSS_LIB = os.path.join(self.build_dir, 'bin')
        config.VTKTUDOSS_PYTHON = os.path.join(
            self.build_dir, 'Wrapping/Python')
 
    def clean_build(self):
        # nuke the build dir, the source dir is pristine and there is
        # no installation
        utils.output("Removing build dir.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
