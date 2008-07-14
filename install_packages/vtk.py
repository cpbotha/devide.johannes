# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import sys
import utils

# cvs -d :pserver:anonymous@public.kitware.com:/cvsroot/VTK login 
# password vtk
#  cvs -d :pserver:anonymous@public.kitware.com:/cvsroot/VTK checkout
#  VTK
# cd VTK
# cvs -z3 update -R blahblah

BASENAME = "VTK"
# password "vtk" integrated in CVS -d spec
CVS_REPO = ":pserver:anonymous:vtk@public.kitware.com:/cvsroot/" + BASENAME
CVS_VERSION = "-r ParaView-3-2-1" # 
# for this tag of VTK, you also need to update wxVTKRWI.py to 1.28
# (fix should be in VTK-5-2 when it gets branched)

VTK_BASE_VERSION = "vtk-5.1"

PDIR1 = \
"http://visualisation.tudelft.nl/~cpbotha/files/vtk_itk/patches/"

# this patch does two things:
# 1. adds try/catch blocks to all python method calls in order
#    to trap bad_alloc exceptions
# 2. implements my scheme for turning all VTK errors into Python exceptions
#    by making use of a special output window class
EXC_PATCH = "pyvtk_tryexcept_and_pyexceptions_20071106.diff"
EXC_PATCH_URL = PDIR1 + EXC_PATCH

# fixes attributes in vtkproperty for shader use in python
VTKPRPRTY_PATCH = "vtkProperty_PyShaderVar.diff"
VTKPRPRTY_PATCH_URL = PDIR1 + VTKPRPRTY_PATCH

# fixes mouse capture brokenness in ParaView-3-2-1 VTK
# will commit this to VTK head with the week (20080229)
WXRWI_CAPTURE_PATCH = "wxVTKRWI_mouse_capture.diff"
WXRWI_CAPTURE_PATCH_URL = PDIR1 + WXRWI_CAPTURE_PATCH

dependencies = []
                  
class VTK(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.archive_dir, BASENAME)
        self.build_dir = os.path.join(config.build_dir, '%s-build' %
                                      (BASENAME,))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)
        self.exc_patch_filename = os.path.join(config.archive_dir,
                                               EXC_PATCH)
        self.vtkprprty_patch_filename = os.path.join(config.archive_dir,
                                                 VTKPRPRTY_PATCH)
        self.wxrwi_capture_patch_filename = os.path.join(
                config.archive_dir, WXRWI_CAPTURE_PATCH)

    def update_wpvi(self):
        """Update Wrapping/Python/vtk/__init__.py to fix nasty DL bug
        on AMD64.  Thanks to Mathieu Malaterre for finding this!
        """

        utils.output("Updating Wrapping/Python/vtk/__init__.py.")

        utils.goto_archive()
        os.chdir(os.path.join(BASENAME, 'Wrapping', 'Python', 'vtk'))

        ret1 = os.system(
        "%s -z3 update -r 1.14 __init__.py" %
        (config.CVS,))

        if ret1 != 0:
            utils.error("Error updating W/P/v/__init__.py.")


    def update_mip(self):
        """Update vtkMedicalImageProperties files to GDCM2-compatible
        versions.
        """
        # we have to update two files to specific versions for
        # GDCM2 VTK support ##################################
        utils.output("Updating vtkMedicalImageProperties.")

        utils.goto_archive()
        os.chdir(os.path.join(BASENAME, 'IO'))

        ret1 = os.system(
        "%s -z3 update -r 1.29 vtkMedicalImageProperties.cxx" %
        (config.CVS,))

        ret2 = os.system(
        "%s -z3 update -r 1.23 vtkMedicalImageProperties.h" %
        (config.CVS,))

        if ret1 != 0 or ret2 != 0:
            utils.error("Error updating vtkMedicalImageProperties.")

        # end of vtkMedicalImageProperties update #############

    def update_ta3d(self):
        """Update vtkTextActor3D to DeVIDE-compatible versions (fixed
        by yours truly in VTK CVS).
        """

        utils.output("Updating vtkTextActor3D.")

        utils.goto_archive()
        os.chdir(os.path.join(BASENAME, 'Rendering'))

        ret1 = os.system(
        "%s -z3 update -r 1.9 vtkTextActor3D.cxx" %
        (config.CVS,))

        ret2 = os.system(
        "%s -z3 update -r 1.4 vtkTextActor3D.h" %
        (config.CVS,))

        if ret1 != 0 or ret2 != 0:
            utils.error("Error updating vtkTextActor3D.")

        # end of vtkTextActor3D update #############

    def update_wxvtkrwi(self):
        """Update wxVTKRenderWindowInteractor to latest fixed version.
        """

        utils.output("Updating wxVTKRenderWindowInteractor.")

        utils.goto_archive()
        os.chdir(os.path.join(BASENAME, 'Wrapping','Python','vtk','wx'))

        ret1 = os.system(
        "%s -z3 update -r 1.28 wxVTKRenderWindowInteractor.py" %
        (config.CVS,))

        if ret1 != 0:
            utils.error("Error updating wxVTKRenderWindowInteractor.")

    def update_vtkoglprop(self):
        """Update vtkOpenGLProperty to DeVIDE-compatible versions (fixed
        by yours truly in VTK CVS).
        """

        utils.output("Updating vtkOpenGLProperty.")

        utils.goto_archive()
        os.chdir(os.path.join(BASENAME, 'Rendering'))

        ret1 = os.system(
        "%s -z3 update -r 1.42 vtkOpenGLProperty.cxx" %
        (config.CVS,))

        if ret1 != 0:
            utils.error("Error updating vtkOpenGLProperty.")

    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("VTK already checked out, skipping step.")

        else:
            utils.goto_archive()
            ret = os.system("%s -d %s co %s %s" %
                            (config.CVS, CVS_REPO, CVS_VERSION, BASENAME))
            if ret != 0:
                utils.error("Could not CVS checkout.  Fix and try again.")

            self.update_wpvi()
            self.update_mip()    
            self.update_ta3d()
            self.update_vtkoglprop()
            self.update_wxvtkrwi()

        if not os.path.exists(self.exc_patch_filename):
            utils.goto_archive()
            utils.urlget(EXC_PATCH_URL)

            # EXC PATCH
            utils.output("Applying EXC patch")
            os.chdir(self.source_dir)
            ret = os.system(
                "%s -p0 < %s" % (config.PATCH, self.exc_patch_filename))
            if ret != 0:
                utils.error(
                    "Could not apply EXC patch.  Fix and try again.")

        if not os.path.exists(self.vtkprprty_patch_filename):
            utils.goto_archive()
            utils.urlget(VTKPRPRTY_PATCH_URL)

            # VTKPRPRTY PATCH
            utils.output("Applying VTKPRPRTY patch")
            os.chdir(os.path.join(self.source_dir, 'Rendering'))
            ret = os.system(
                "%s -p0 < %s" % (config.PATCH, self.vtkprprty_patch_filename))
            if ret != 0:
                utils.error(
                    "Could not apply VTKPRPRTY patch.  Fix and try again.")

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
            config.VTK_SODIR = config.VTK_LIB
            # on *ix, inst/lib/python2.5/site-packages contains the
            # VTK python package
            # sys.version is (2, 5, 0, 'final', 0)
            config.VTK_PYTHON = os.path.join(
                config.VTK_LIB, 'python%d.%d/site-packages' % \
                sys.version_info[0:2])

        # this contains the VTK cmake config (same on *ix and Win)
        config.VTK_DIR = os.path.join(config.VTK_LIB, VTK_BASE_VERSION)


        posix_file = os.path.join(self.inst_dir, 'bin/vtkpython')
        nt_file = os.path.join(self.inst_dir, 'bin', 'vtkpython.exe')

        if utils.file_exists(posix_file, nt_file):    
            utils.output("VTK already installed.  Skipping build step.")

        else:
            # python 2.5.2 setup.py complains that this does not exist
            # with VTK PV-3-2-1.  This is only on installations with
            # EasyInstall / Python Eggs, then the VTK setup.py uses
            # EasyInstall and not standard distutils.  gah!
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


        
    def clean_build(self):
        utils.output("Removing build and installation directories.")
        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)

        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        
