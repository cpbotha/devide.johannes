import config
from install_package import InstallPackage
import os
import shutil
import utils

BASENAME = "CableSwig"
CVS_REPO = ":pserver:anonymous@www.itk.org:/cvsroot/" + BASENAME
CVS_VERSION = "-D 20061008"

class CableSwig(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.build_dir, BASENAME)
        self.build_dir = os.path.join(config.build_dir, '%s-build' %
                                      (BASENAME,))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)

    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("CableSwig already checked out, skipping step.")

        else:
            os.chdir(config.build_dir)
            ret = os.system("%s -d %s co %s %s" %
                            (config.CVS, CVS_REPO, CVS_VERSION, BASENAME))
            
            if ret != 0:
                utils.error("Could not CVS checkout.  Fix and try again.")
