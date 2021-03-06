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

BASENAME = "VTK"
GIT_REPO = "http://vtk.org/VTK.git"
GIT_TAG = "v5.8.0"

VTK_BASE_VERSION = "vtk-5.8"

# this patch does three things:
# 1. adds try/catch blocks to all python method calls in order
#    to trap bad_alloc exceptions
# 2. implements my scheme for turning all VTK errors into Python exceptions
#    by making use of a special output window class
# 3. gives up the GIL around all VTK calls.  This is also necessary
#    for 2 not to deadlock on multi-cores.
EXC_PATCH = "pyvtk580_tryexcept_and_pyexceptions.diff"

# fixes attributes in vtkproperty for shader use in python
VTKPRPRTY_PATCH = "vtkProperty_PyShaderVar.diff"

# recent segfault with vtk 5.6.1 and wxPython 2.8.11.0
# see here for more info:
# http://vtk.1045678.n5.nabble.com/wx-python-scripts-segfault-td1234471.html  
WXVTKRWI_DISPLAYID_SEGFAULT_PATCH = "wxvtkrwi_displayid_segfault.diff"

dependencies = ['CMake']
                  
class VTK58(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.archive_dir, BASENAME)
        self.build_dir = os.path.join(config.build_dir, '%s-build' %
                                      (BASENAME,))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)
        self.exc_patch_src = os.path.join(config.patches_dir, EXC_PATCH)
        self.exc_patch_dst = os.path.join(config.archive_dir, EXC_PATCH)
        self.vtkprprty_patch_filename = os.path.join(config.patches_dir,
                                                 VTKPRPRTY_PATCH)

        self.wxvtkrwi_displayid_segfault_patch_filename = os.path.join(
                config.patches_dir,
                WXVTKRWI_DISPLAYID_SEGFAULT_PATCH)

        config.VTK_LIB = os.path.join(self.inst_dir, 'lib')

        # whatever the case may be, we have to register VTK variables
        if os.name == 'nt':
            # on Win, inst/VTK/bin contains the so files
            config.VTK_SODIR = os.path.join(self.inst_dir, 'bin')
            # inst/VTK/lib/site-packages the VTK python package
            config.VTK_PYTHON = os.path.join(
                    config.VTK_LIB, 'site-packages')

        else:
            # on *ix, inst/VTK/lib contains DLLs
            config.VTK_SODIR = os.path.join(
                    config.VTK_LIB, VTK_BASE_VERSION)
            # on *ix, inst/lib/python2.5/site-packages contains the
            # VTK python package
            # sys.version is (2, 5, 0, 'final', 0)
            config.VTK_PYTHON = os.path.join(
                config.VTK_LIB, 'python%d.%d/site-packages' % \
                sys.version_info[0:2])

        # this contains the VTK cmake config (same on *ix and Win)
        config.VTK_DIR = os.path.join(config.VTK_LIB, VTK_BASE_VERSION)

    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("VTK already checked out, skipping step.")

        else:
            utils.goto_archive()

            ret = os.system("git clone %s %s" % (GIT_REPO, BASENAME))
            if ret != 0:
                utils.error("Could not clone VTK repo.  Fix and try again.")

            os.chdir(self.source_dir)
            ret = os.system("git checkout %s" % (GIT_TAG,))
            if ret != 0:
                utils.error("Could not checkout VTK %s. Fix and try again." % (GIT_TAG,))


        if not os.path.exists(self.exc_patch_dst):
            utils.output("Applying EXC patch")
            # we do this copy so we can see if the patch has been done yet or not
            shutil.copyfile(self.exc_patch_src, self.exc_patch_dst)

            os.chdir(self.source_dir)
            # default git-generated patch, so needs -p1
            ret = os.system(
                "%s -p1 < %s" % (config.PATCH, self.exc_patch_dst))

            if ret != 0:
                utils.error(
                    "Could not apply EXC patch.  Fix and try again.")

            # # VTKPRPRTY PATCH
            # utils.output("Applying VTKPRPRTY patch")
            # os.chdir(os.path.join(self.source_dir, 'Rendering'))
            # ret = os.system(
                # "%s -p0 < %s" % (config.PATCH, self.vtkprprty_patch_filename))
            # if ret != 0:
                # utils.error(
                    # "Could not apply VTKPRPRTY patch.  Fix and try again.")

            # # WXVTKRWI_DISPLAYID_SEGFAULT patch
            # utils.output("Applying VTKWXRWI_DISPLAYID_SEGFAULT patch")
            # os.chdir(self.source_dir)
            # # default git-generated patch, so needs -p1
            # ret = os.system(
                # "%s -p1 < %s" % (config.PATCH, 
                    # self.wxvtkrwi_displayid_segfault_patch_filename))
            # if ret != 0:
                # utils.error(
                    # "Could not apply WXVTKRWI_DISPLAYID_SEGFAULT patch.  Fix and try again.")


    def unpack(self):
        pass               
                
    def configure(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'CMakeFiles/cmake.check_cache')):
            utils.output("VTK build already configured.")
            return
        
        if not os.path.exists(self.build_dir):
            os.mkdir(self.build_dir)

        cmake_params = "-DBUILD_SHARED_LIBS=ON " \
                       "-DBUILD_TESTING=OFF " \
                       "-DCMAKE_BUILD_TYPE=RelWithDebInfo " \
                       "-DCMAKE_INSTALL_PREFIX=%s " \
		               "-DVTK_USE_TK=NO " \
                       "-DVTK_USE_METAIO=ON " \
                       "-DVTK_USE_PARALLEL=ON " \
                       "-DPYTHON_EXECUTABLE=%s " \
                       "-DPYTHON_LIBRARY=%s " \
                       "-DPYTHON_INCLUDE_PATH=%s " \
                       "-DVTK_WRAP_PYTHON=ON " % (self.inst_dir,
                                                 config.PYTHON_EXECUTABLE,
                                                 config.PYTHON_LIBRARY,
                                                 config.PYTHON_INCLUDE_PATH)

        ret = utils.cmake_command(self.build_dir, self.source_dir,
                cmake_params)

        if ret != 0:
            utils.error("Could not configure VTK.  Fix and try again.")
                       

    def build(self):
        posix_file = os.path.join(self.build_dir,
            'bin/libvtkWidgetsPython.so')
        nt_file = os.path.join(self.build_dir, 'bin', config.BUILD_TARGET, 
                'vtkWidgetsPythonD.dll')

        if utils.file_exists(posix_file, nt_file):
            utils.output("VTK already built.  Skipping build step.")

        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('VTK.sln')
            if ret != 0:
                utils.error("Error building VTK.  Fix and try again.")

    def install(self):
        posix_file = os.path.join(self.inst_dir, 'bin/vtkpython')
        nt_file = os.path.join(self.inst_dir, 'bin', 'vtkpython.exe')

        if utils.file_exists(posix_file, nt_file):    
            utils.output("VTK already installed.  Skipping build step.")

        else:
            # python 2.5.2 setup.py complains that this does not exist
            # with VTK PV-3-2-1.  This is only on installations with
            # EasyInstall / Python Eggs, then the VTK setup.py uses
            # EasyInstall and not standard distutils.  gah!
            
            # just tested with VTK 5.8.0 and Python 2.7.2
            # it indeed installs VTK_PYTHON/VTK-5.8.0-py2.7.egg
            # but due to the site.py and easy-install.pth magic in there,
            # adding VTK_PYTHON to the PYTHONPATH still works. We can keep
            # pip, yay!
            if not os.path.exists(config.VTK_PYTHON):
                os.makedirs(config.VTK_PYTHON)

            os.chdir(self.build_dir)

            # we save, set and restore the PP env variable, else
            # stupid setuptools complains
            save_env = os.environ.get('PYTHONPATH', '')
            os.environ['PYTHONPATH'] = config.VTK_PYTHON
            ret = utils.make_command('VTK.sln', install=True)
            os.environ['PYTHONPATH'] = save_env

            if ret != 0:
                utils.error("Could not install VTK.  Fix and try again.")

            # now do some surgery on VTKConfig.cmake and
            # VTKLibraryDepends.cmake so builds of VTK-dependent libraries
            # with only the DRE to link with Just Work(tm)

            # on windows, we need to replace backslash with forward slash
            # as that's the style used by the config files. On *ix mostly
            # harmless
            idp = re.sub(r'\\','/', config.inst_dir)
            for fn in [os.path.join(config.VTK_DIR, 'VTKConfig.cmake'),
                    os.path.join(config.VTK_DIR, 'VTKLibraryDepends.cmake'),
                    os.path.join(config.VTK_DIR, 'VTKTargets-relwithdebinfo.cmake')]:
                if os.path.exists(fn):
                    utils.re_sub_filter_file(
                            [(idp,  '${VTK_INSTALL_PREFIX}/..')], 
                            fn)



        
    def clean_build(self):
        utils.output("Removing build and installation directories.")
        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)

        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        
    def clean_install(self):
        utils.output("Removing installation directory.")
        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)
    
    def get_installed_version(self):
        import vtk
        return vtk.vtkVersion.GetVTKVersion()

        
