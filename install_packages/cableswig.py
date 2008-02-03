
# since ITK 3.4 (perhaps earlier) you do NOT HAVE TO BUILD CABLESWIG
# separately.  This install package is on ice.  DO NOT USE.


import config
from install_package import InstallPackage
import os
import shutil
import utils
import sys

BASENAME = "CableSwig"
# password part of REPO spec
CVS_REPO = ":pserver:anonymous@www.itk.org:/cvsroot/" + BASENAME
CVS_VERSION = "-r ITK-3-4" # 

class CableSwig(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.archive_dir, BASENAME)
        self.build_dir = os.path.join(config.build_dir, '%s-build' %
                                      (BASENAME,))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)

    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("CableSwig already checked out, skipping step.")

        else:
            os.chdir(config.archive_dir)
            ret = os.system("%s -d %s co %s %s" %
                            (config.CVS, CVS_REPO, CVS_VERSION, BASENAME))
            
            if ret != 0:
                utils.error("Could not CVS checkout.  Fix and try again.")

    def unpack(self):
        pass

    def configure(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'CMakeFiles/cmake.check_cache')):
            utils.output("CableSwig build already configured.")
            return
        
        if not os.path.exists(self.build_dir):
            os.mkdir(self.build_dir)

        os.chdir(self.build_dir)
        cmake_params = "-DBUILD_TESTING=OFF " \
                       "-DCMAKE_BUILD_TYPE=RelWithDebInfo " \
                       "-DCMAKE_INSTALL_PREFIX=%s " \
                      % (self.inst_dir,)

        ret = os.system("%s %s %s" %
                        (config.CMAKE, cmake_params, self.source_dir))

        if ret != 0:
            utils.error("Could not configure CableSwig.  Fix and try again.")

    def build(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'bin/cswig')):
            utils.output("CableSwig already built.  Skipping build step.")

        else:
            os.chdir(self.build_dir)
            ret = os.system("%s" % (config.MAKE,))
            if ret != 0:
                utils.error("Error building CableSwig.  Fix and try again.")

    def install(self):
        # directory containing cmake config + bin dir
        config.CABLESWIG_DIR = os.path.join(self.inst_dir, \
        'lib/CableSwig')

        if os.path.exists(
            os.path.join(config.CABLESWIG_DIR, 'CableSwigConfig.cmake')):
            utils.output("CableSwig already installed.  Skipping step.")

        else:
            os.chdir(self.build_dir)
            ret = os.system("%s install" % (config.MAKE,))
            if ret != 0:
                utils.error("Could not install CableSwig.  Fix and try again.")


    def clean_build(self):
        utils.output("Removing build and installation directories.")
        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)

        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

        

        
