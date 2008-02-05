import config
from install_package import InstallPackage
import os
import shutil
import sys
import utils

# NB: for this module to build successfully, ITK has to be built with
#     ITK_USE_REVIEW=ON (until the itkFlatStructuringElement moves OUT of the
#     review directory, that is)

BASENAME = "itktudoss"
SVN_REPO = "http://itktudoss.googlecode.com/svn/trunk/"
SVN_REL = config.ITKTUDOSS_REL

class ITKTUDOSS(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.archive_dir, BASENAME)
        self.build_dir = os.path.join(config.build_dir, '%s-build' %
                                      (BASENAME,))

    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("itktudoss already checked out, skipping step.")

        else:
            os.chdir(config.archive_dir)
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
            utils.output("itktudoss build already configured.")
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
                       "-DWrapITK_DIR:PATH=%s " \
                       "-DPYTHON_EXECUTABLE=%s " \
                       % \
                       (config.ITK_INSTALL_PREFIX,
                        config.ITK_DIR, config.WRAPITK_DIR,
                        sys.executable)

        ret = utils.cmake_command(self.build_dir, self.source_dir,
                cmake_params)

        if ret != 0:
            utils.error(
                "Could not configure itktudoss.  Fix and try again.")


    def build(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'lib/_itktudossPython.so')):

            utils.output("itktudoss already built.  Skipping build step.")

        else:
            os.chdir(self.build_dir)
            ret = os.system("%s" % (config.MAKE,))
            if ret != 0:
                utils.error("Could not build itktudoss.  Fix and try again.")
        

    def install(self):
        #config.VTKTUD_LIB = os.path.join(self.build_dir, 'bin')
        #config.VTKTUD_PYTHON = os.path.join(
        #    self.source_dir, 'Wrapping/Python')

        if os.path.exists(
            os.path.join(config.WRAPITK_LIB, '_itktudossPython.so')):
            utils.output("itktudoss already installed.  Skipping step.")

        else:
            os.chdir(self.build_dir)
            ret = os.system("%s install" % (config.MAKE,))
            if ret != 0:
                utils.error(
                    "Could not install itktudoss.  Fix and try again.")

 
    def clean_build(self):
        # nuke the build dir, the source dir is pristine and there is
        # no installation
        utils.output("Removing build dir.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

        inst_so = os.path.join(config.WRAPITK_LIB, '_itktudossPython.so')
        if os.path.exists(inst_so):
            os.remove(inst_so)

