import config
from install_package import InstallPackage
import os
import shutil
import utils
import sys

BASENAME = "Insight"
# password part of REPO spec
CVS_REPO = ":pserver:anonymous:insight@www.itk.org:/cvsroot/" + BASENAME
CVS_VERSION = "-D 20061008"

CABLESWIG_REPO = ":pserver:anonymous@www.itk.org:/cvsroot/CableSwig"
CABLESWIG_VERSION = "-D 20061008"

class ITK(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.build_dir, BASENAME)
        self.build_dir = os.path.join(config.build_dir, '%s-build' %
                                      (BASENAME,))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)

    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("ITK already checked out, skipping step.")

        else:
            os.chdir(config.build_dir)
            ret = os.system("%s -d %s co %s %s" %
                            (config.CVS, CVS_REPO, CVS_VERSION, BASENAME))
            
            if ret != 0:
                utils.error("Could not CVS checkout.  Fix and try again.")


        utilities_dir = os.path.join(self.source_dir, 'Utilities')
        cableswig_source_dir = os.path.join(utilities_dir,
                                            'CableSwig')
        
        if os.path.exists(cableswig_source_dir):
            utils.output("CableSwig already checked out, skipping step.")

        else:
            os.chdir(utilities_dir)
            ret = os.system("%s -d %s co %s %s" %
                            (config.CVS, CABLESWIG_REPO, CABLESWIG_VERSION,
                             "CableSwig"))

            if ret != 0:
                utils.error(
                    "Could not CVS checkout CableSwig.  Fix and try again.")

    def unpack(self):
        pass

    def configure(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'CMakeFiles/cmake.check_cache')):
            utils.output("ITK build already configured.")
            return
        
        if not os.path.exists(self.build_dir):
            os.mkdir(self.build_dir)

        os.chdir(self.build_dir)
        cmake_params = "-DBUILD_EXAMPLES=OFF " \
                       "-DBUILD_SHARED_LIBS=ON " \
                       "-DBUILD_TESTING=OFF " \
                       "-DCMAKE_BUILD_TYPE=RelWithDebInfo " \
                       "-DCMAKE_INSTALL_PREFIX=%s " \
                       "-DUSE_WRAP_ITK=ON " \
                       "-DINSTALL_WRAP_ITK_COMPATIBILITY=OFF " \
                       "-DPYTHON_INCLUDE_PATH=%s " \
                       "-DPYTHON_LIBRARY=%s " \
                       "-DPYTHON_EXECUTABLE=%s " \
                       "-DWRAP_ITK_PYTHON=ON " \
                       "-DWRAP_ITK_TCL=OFF " \
                       "-DWRAP_ITK_JAVA=OFF " \
                       "-DWRAP_unsigned_short=OFF " \
                       "-DWRAP_signed_short=ON " \
                       % (self.inst_dir,
                          config.python_include_path, config.python_library,
                          sys.executable)

        ret = os.system("%s %s %s" %
                        (config.CMAKE, cmake_params, self.source_dir))

        if ret != 0:
            utils.error("Could not configure ITK.  Fix and try again.")

    def build(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'bin/_RegistrationPython.so')):
            utils.output("ITK already built.  Skipping build step.")

        else:
            os.chdir(self.build_dir)
            ret = os.system("%s" % (config.MAKE,))
            if ret != 0:
                utils.error("Error building ITK.  Fix and try again.")

    def install(self):
        # this is the dir with the cmake config as well as all binaries
        config.ITK_DIR = os.path.join(self.inst_dir, 'lib/InsightToolkit')
        config.WRAPITK_DIR = os.path.join(config.ITK_DIR, 'WrapITK')
        # contains all WrapITK shared objects / libraries
        config.WRAPITK_LIB = os.path.join(config.WRAPITK_DIR, 'lib')
        # contains itk.py
        config.WRAPITK_PYTHON = os.path.join(config.WRAPITK_DIR, 'Python')
        
        if os.path.exists(
            os.path.join(config.WRAPITK_LIB, '_UnaryPixelMathPython.so')):
            utils.output("ITK already installed.  Skipping step.")

        else:
            os.chdir(self.build_dir)
            ret = os.system("%s install" % (config.MAKE,))
            if ret != 0:
                utils.error("Could not install ITK.  Fix and try again.")


    def clean_build(self):
        utils.output("Removing build and installation directories.")
        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)

        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

        

        
