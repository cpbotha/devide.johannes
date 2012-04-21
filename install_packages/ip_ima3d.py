# Copyright (c) Francois Malan & Christian Kehl, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import utils
from subprocess import call

BASENAME = "IMA3d"

#The original unmodified IMA3d code excludes Christian's changes (e.g. handling .mhd files), and can be found at http://www.cs.rug.nl/~roe/software/IMA/IMA3d.tgz
HG_REPO  = "https://hg.graphics.tudelft.nl/vis/christian/ima3d"

dependencies = []

class IMA3d(InstallPackage):
    """ Integer Medial Axis described in the paper
    W. H. Hesselink, J. B. T. M. Roerdink: Euclidean skeletons of digital image and volume data in linear time by integer medial axis transform. IEEE Trans. Pattern Anal. Machine Intell. 30 (2008) 2204--2217.
    
    When you use the code, please refer to the above paper, its authors, and the University of Groningen.
    
    This code has been modified & extended by Christian Kehl - the original version can be found at http://www.cs.rug.nl/~roe/software/IMA/IMA3d.tgz
    """
    
    def __init__(self):
        self.source_dir = os.path.join(config.archive_dir, '%s' %
                                      (BASENAME,))
        self.build_dir = os.path.join(config.build_dir, '%s' %
                                      (BASENAME,))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)
    
    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("%s already checked out, skipping step." % BASENAME)            
        
        else:
            os.chdir(config.archive_dir)
            ret = os.system("%s clone %s" % (config.HG, HG_REPO))
            if ret != 0:
                utils.error("Could check out %s using HG. Fix and try again." % BASENAME)
                return   
        
    def unpack(self):
        # no unpack step
        pass
        
    def configure(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'CMakeFiles/cmake.check_cache')):
            utils.output("%s build already configured." % BASENAME)
            return
        
        if not os.path.exists(self.build_dir):
            os.mkdir(self.build_dir)

        cmake_params = "-DCMAKE_BUILD_TYPE=RelWithDebInfo " \
                       "-DCMAKE_INSTALL_PREFIX=%s " \
                        % (self.inst_dir,)

        ret = utils.cmake_command(self.build_dir, self.source_dir,
                cmake_params)

        if ret != 0:
            utils.error(
                "Could not configure %s.  Fix and try again." % BASENAME)   
    
    def build(self):
        bin_path = os.path.join(self.build_dir,'src','multisurfaces','run-particle-system','optimize-particle-system.dir')

        if utils.file_exists(bin_path, bin_path):    
            utils.output("%s already built.  Skipping build step." % BASENAME)

        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('%s.sln' % BASENAME)

            if ret != 0:
                utils.error("Could not build %s.  Fix and try again." % BASENAME)
    
    def get_installed_version(self):
        return "N/A"