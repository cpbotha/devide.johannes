# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import re
import shutil
import sys
import utils

BASENAME = "OrthoAssist"
GIT_REPO = "https://thomas@hg.graphics.tudelft.nl/vis/thomas/OrthoAssist"
#GIT_TAG = "v5.6.1"

dependencies = ['CMake','Qt','VTK58','SIP','PyQt']
                  
class OrthoAssist(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.archive_dir, BASENAME)
        self.build_dir = os.path.join(config.build_dir, '%s' % (BASENAME,))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)
    
    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("Ortho Assist already checked out, skipping step.")

        else:
            utils.goto_archive()
            
            ret = os.system("hg clone %s %s" % (GIT_REPO, BASENAME))
            if ret != 0:
                utils.error("Could not clone Ortho Assist repository.  Fix and try again.")
            
            os.chdir(self.source_dir)
            ret = os.system("hg update")
            if ret != 0:
                utils.error("Could not update Ortho Assist. Fix and try again.")

    def configure(self):
        pass
		
    def build(self):
        pass

    def install(self):
        pass
        
    def clean_build(self):
        pass
        
    def clean_install(self):
        pass
    
    def get_installed_version(self):
		pass
		