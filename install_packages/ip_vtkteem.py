# Copyright (c) Francois Malan & Christian Kehl, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import utils
from subprocess import call

REVISION_NUMBER = "8877"
BASENAME = "vtkTeem"
SVN_REPO = "http://svn.slicer.org/Slicer3/trunk/Libs/vtkTeem"

dependencies = ['CMake', 'VTK58', 'Teem']

# this patch makes the necessary changes that enables building vtkTeem.
# These changes are explained in: http://code.google.com/p/devide/wiki/AddingVTKTeem
# This mainly involves replacing the default TCL wrappings with Python wrappings 
TCL_PY_PATCH = "vtkteem_cmakelists_python_instead_of_tcl.diff"

class vtkTeem(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.archive_dir, '%s' %
                                      (BASENAME,))
        self.build_dir = os.path.join(config.build_dir, '%s' %
                                      (BASENAME,))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)
        self.tcl_py_patch_src = os.path.join(config.patches_dir, TCL_PY_PATCH)
        self.tcl_py_patch_dst = os.path.join(self.source_dir, TCL_PY_PATCH)        

    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("%s already checked out, skipping step." % BASENAME)            
        
        else:
            os.chdir(config.archive_dir)
            ret = call("%s co %s -r %s %s" % \
                (config.SVN, SVN_REPO, REVISION_NUMBER, BASENAME), shell=True)
            if ret != 0:
                utils.error("Could not SVN checkout. Fix and try again.")
                return                
        
        if not os.path.exists(self.tcl_py_patch_dst):
            utils.output("Applying TCL -> Python patch")
            # we do this copy so we can see if the patch has been done yet or not
            shutil.copyfile(self.tcl_py_patch_src, self.tcl_py_patch_dst)        
            
            os.chdir(self.source_dir)
            # default git-generated patch, so needs -p1
            ret = os.system(
                "%s < %s" % (config.PATCH, TCL_PY_PATCH))

            if ret != 0:
                utils.error(
                    "Could not apply TCL -> Python patch.  Fix and try again.")
                    
    def unpack(self):
        # no unpack step
        pass

    def configure(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'CMakeFiles/cmake.check_cache')):
            utils.output("vtkTeem build already configured.")
            return
        
        if not os.path.exists(self.build_dir):
            os.mkdir(self.build_dir)

        cmake_params = "-DCMAKE_BUILD_TYPE=RelWithDebInfo " \
                       "-DCMAKE_INSTALL_PREFIX=%s " \
                       "-DVTK_DIR=%s " \
                       "-DTeem_DIR=%s " \
                        % \
                       (self.inst_dir,config.VTK_DIR,config.Teem_DIR)
                       
        ret = utils.cmake_command(self.build_dir, self.source_dir,
                cmake_params)

        if ret != 0:
            utils.error(
                "Could not configure vtkTeem.  Fix and try again.")

    def build(self):
        nt_file = os.path.join(self.build_dir, 
                'vtkTeemInit.cxx')

        if utils.file_exists(nt_file, nt_file):    
            utils.output("vtkTeem already built.  Skipping build step.")

        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('vtkTeem.sln')

            if ret != 0:
                utils.error("Could not build vtkTeem.  Fix and try againn.")
    
    def install(self):
        if os.path.exists(
            os.path.join(self.inst_dir, 'bin', 
                'vtkTeem' + config.SO_EXT)):
            utils.output("vtkTeem already installed.  Skipping step.")

        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('vtkTeem.sln', install=True)

            if ret != 0:
                utils.error(
                    "Could not install vtkTeem. Fix and try again.")
 
    def clean_build(self):
        # nuke the build dir and install dir. The source dir is pristine
        
        utils.output("Removing build dir.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

        utils.output("Removing install dir.")
        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)

    def get_installed_version(self):
        return "revision %s" % REVISION_NUMBER

