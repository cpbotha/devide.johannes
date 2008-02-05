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

    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("VTK already checked out, skipping step.")

        else:
            utils.goto_archive()
            ret = os.system("%s -d %s co %s %s" %
                            (config.CVS, CVS_REPO, CVS_VERSION, BASENAME))
            if ret != 0:
                utils.error("Could not CVS checkout.  Fix and try again.")

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
                       "-DVTK_USE_METAIO=ON" \
                       "-DVTK_USE_PARALLEL=ON" \
                       "-DPYTHON_EXECUTABLE=%s " \
                       "-DVTK_WRAP_PYTHON=ON" % (self.inst_dir,
                                                 sys.executable)

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
            os.chdir(self.build_dir)
            # with VTK ParaView-3-2-1 on Windows, I had to run the
            # installer twice.  The first time, it quit (without
            # detectable errors) whilst copying vtkBYUReader.h!
            ret = utils.make_command('VTK.sln', install=True)
            if ret != 0:
                utils.error("Could not install VTK.  Fix and try again.")

        # whatever the case may be, we have to register VTK variables
        config.VTK_LIB = os.path.join(self.inst_dir, 'lib')
        # sys.version is (2, 5, 0, 'final', 0)
        config.VTK_PYTHON = os.path.join(
            config.VTK_LIB, 'python%d.%d/site-packages' % \
            sys.version_info[0:2])
        # this contains the VTK cmake config
        config.VTK_DIR = os.path.join(config.VTK_LIB, VTK_BASE_VERSION)
        
    def clean_build(self):
        utils.output("Removing build and installation directories.")
        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)

        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        
