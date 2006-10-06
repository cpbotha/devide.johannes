import config
from install_package import InstallPackage
import os
import utils

VTK_TARBALL = "vtk-5.0.2.tar.gz"
VTK_URL = "http://www.vtk.org/files/release/5.0/%s" % (VTK_TARBALL,)
VTK_DIRBASE = "VTK"

# this patch does two things:
# 1. adds try/catch blocks to all python method calls in order
#    to trap bad_alloc exceptions
# 2. implements my scheme for turning all VTK errors into Python exceptions
#    by making use of a special output window class
EXC_PATCH = "pyvtk_tryexcept_and_pyexceptions_20061006.diff"
EXC_PATCH_URL = "http://visualisation.tudelft.nl/~cpbotha/thingies/" + \
                  EXC_PATCH

# gcc 4.0 errors on some trivial assignment of const char * to char *
# this patch fixes that so that VTK 5.0.2 builds on gcc 4 systems
GCC40_PATCH = "vtk502_gcc40_pythonutil.diff"
GCC40_PATCH_URL = "http://visualisation.tudelft.nl/~cpbotha/thingies/" + \
                  GCC40_PATCH
                  
class VTK(InstallPackage):
    
    def __init__(self):
        self.tbfilename = os.path.join(config.archive_dir, VTK_TARBALL)
        self.source_dir = os.path.join(config.build_dir, VTK_DIRBASE)
        self.build_dir = os.path.join(config.build_dir, '%s-build' %
                                      (VTK_DIRBASE,))
        self.inst_dir = os.path.join(config.inst_dir, 'VTK')
        self.exc_patch_filename = os.path.join(config.archive_dir,
                                               EXC_PATCH)
        self.gcc40_patch_filename = os.path.join(config.archive_dir,
                                                 GCC40_PATCH)

    def get(self):
        if os.path.exists(self.tbfilename):
            utils.output("%s already present, not downloading." %
                         (VTK_TARBALL,))
        else:
            utils.goto_archive()
            utils.urlget(VTK_URL)

        if not os.path.exists(self.exc_patch_filename):
            utils.goto_archive()
            utils.urlget(EXC_PATCH_URL)

        if not os.path.exists(self.gcc40_patch_filename):
            utils.goto_archive()
            utils.urlget(GCC40_PATCH_URL)
            

    def unpack(self):
        if os.path.isdir(self.source_dir):
            utils.output("VTK source already unpacked, not redoing.")
        else:
            utils.output("Unpacking VTK source.")
            utils.unpack_build(self.tbfilename)

            # EXC PATCH
            utils.output("Applying EXC patch")
            os.chdir(self.source_dir)
            ret = os.system(
                "%s -p0 < %s" % (config.PATCH, self.exc_patch_filename))
            if ret != 0:
                utils.output(
                    "Could not apply EXC patch.  Fix and try again.")

            # GCC40 patch
            utils.output("Applying GCC40 patch")
            os.chdir(self.source_dir)
            ret = os.system(
                "%s -p0 < %s" % (config.PATCH, self.gcc40_patch_filename))
            if ret != 0:
                utils.output(
                    "Could not apply GCC40 patch.  Fix and try again.")
                
    def configure(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'CMakeFiles/cmake.check_cache')):
            utils.output("VTK build already configured.")
            return
        
        if not os.path.exists(self.build_dir):
            os.mkdir(self.build_dir)

        os.chdir(self.build_dir)
        cmake_params = "-DBUILD_SHARED_LIBS=ON " \
                       "-DBUILD_TESTING=OFF " \
                       "-DCMAKE_BUILD_TYPE=RelWithDebInfo " \
                       "-DCMAKE_INSTALL_PREFIX=%s " \
                       "-DPYTHON_INCLUDE_PATH=%s " \
                       "-DPYTHON_LIBRARY=%s " \
                       "-DVTK_WRAP_PYTHON=ON" % (self.inst_dir,
                                                 config.python_include_path,
                                                 config.python_library)
        
        ret = os.system("%s %s %s" %
                        (config.CMAKE, cmake_params, self.source_dir))

        if ret != 0:
            utils.error("Could not configure VTK.  Fix and try again.")
                       

    def build(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'bin/libvtkWidgetsPython.so')):

            utils.output("VTK already built.  Skipping build step.")

        else:
            os.chdir(self.build_dir)
            ret = os.system("%s" % (config.MAKE,))

    def install(self):
        if os.path.exists(
            os.path.join(self.inst_dir, 'bin/vtkpython')):
            utils.output("VTK already installed.  Skipping build step.")

        else:
            os.chdir(self.build_dir)
            ret = os.system("%s install" % (config.MAKE,))
        
