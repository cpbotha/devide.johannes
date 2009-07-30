# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import sys
import utils
from distutils import sysconfig

MPL_VER = "0.98.5.3"

WIN64 = False

if os.name == 'posix':
    MPL_ARCHIVE = "matplotlib-%s.tar.gz" % (MPL_VER,)
elif os.name == 'nt':
    MPL_ARCHIVE = "matplotlib-%s_r0-py2.6-win32.egg" % (MPL_VER,)

    import platform
    a = platform.architecture()[0]
    if a == '64bit':
        WIN64 = True
 
MPL_URL = "http://surfnet.dl.sourceforge.net/sourceforge/matplotlib/%s" % \
          (MPL_ARCHIVE,)

MPL_DIRBASE = "matplotlib-%s" % (MPL_VER,)

# I prefer that this be built with numpy, but it is not a dependency
# per se
dependencies = []

class matplotlib(InstallPackage):

    def __init__(self):
        self.tbfilename = os.path.join(config.archive_dir, MPL_ARCHIVE)
        self.build_dir = os.path.join(config.build_dir, MPL_DIRBASE)
        self.inst_dir = os.path.join(config.inst_dir, 'matplotlib')

    def get(self):
        if WIN64:
            utils.output("matplotlib not yet supported on Win64.")
            return

        if os.path.exists(self.tbfilename):
            utils.output("%s already present, not downloading." %
                         (MPL_ARCHIVE,))
        else:
            utils.goto_archive()
            utils.urlget(MPL_URL)

    def unpack(self):
        if os.name == 'nt':
            utils.output("Skipping unpack (WINDOWS).")
            return

        if os.path.isdir(self.build_dir):
            utils.output("MATPLOTLIB source already unpacked, not redoing.")
        else:
            utils.output("Unpacking MATPLOTLIB source.")
            utils.unpack_build(self.tbfilename)

    def configure(self):
        if os.name == 'nt':
            utils.output("Skipping configure (WINDOWS).")
            return

        # pre-configure setup.py and setupext.py so that everything is
        # found and configured as we want it.
        os.chdir(self.build_dir)

        if os.path.exists('setup.py.new'):
            utils.output('matplotlib already configured.  Skipping step.')

        else:
            # pre-filter setup.py
            repls = [("(BUILD_GTKAGG\s*=\s*).*", "\\1 0"),
                     ("(BUILD_GTK\s*=\s*).*", "\\1 0"),
                     ("(BUILD_TKAGG\s*=\s*).*", "\\1 0"),
                     ("(BUILD_WXAGG\s*=\s*).*", "\\1 1"),
                     ("(rc\s*=\s*dict\().*",
                      "\\1 {'backend':'PS', 'numerix':'numpy'} )")]

            utils.re_sub_filter_file(repls, 'setup.py')

    def build(self):
        if os.name == 'nt':
            utils.output("Skipping build (WINDOWS).")
            return

        os.chdir(self.build_dir)

        # weak test... there are .so files deeper, but they're in platform
        # specific directories
        if os.path.exists('build'):
            utils.output('matplotlib already built.  Skipping step.')

        else:

            # add wx bin to path so that wx-config can be found
            os.environ['PATH'] = "%s%s%s" % (config.WX_BIN_PATH,
                                             os.pathsep, os.environ['PATH'])
        
            ret = os.system('%s setup.py build' % (sys.executable,))
            
            if ret != 0:
                utils.error('matplotlib build failed.  Please fix and try again.')

    def install(self):
        if WIN64:
            utils.output("matplotlib not yet supported on Win64.")
            return

        # to test for install, just do python -c "import matplotlib"
        # and test the result (we could just import directly, but that would
        # only work once our invoking python has been stopped and started
        # again)
        os.chdir(config.archive_dir) # we need to be elsewhere!
        ret = os.system('%s -c "import matplotlib"' % (sys.executable,))
        if ret == 0:
            utils.output('matplotlib already installed.  Skipping step.')

        else:
            utils.output('ImportError test shows that matplotlib is not '
                         'installed.  Installing...')

            if os.name == 'nt':
                self.install_nt()
            else:
                self.install_posix()

    def install_nt(self):
        sp_dir = sysconfig.get_python_lib()
        os.chdir(sp_dir)
        # on windows, this is an egg file, we simply unpack.
        utils.unpack(self.tbfilename)

        # should we delete the EGG-INFO dir that gets created in site-packages?

    def install_posix(self):
        os.chdir(self.build_dir)
        
        # add wx bin to path so that wx-config can be found
        os.environ['PATH'] = "%s%s%s" % (config.WX_BIN_PATH,
                                         os.pathsep, os.environ['PATH'])

        ret = os.system('%s setup.py install' % (sys.executable,))
        
        if ret != 0:
            utils.error(
                'matplotlib install failed.  Please fix and try again.')

    def clean_build(self):
        utils.output("Removing build and install directories.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

        from distutils import sysconfig
        matplotlib_instdir = os.path.join(sysconfig.get_python_lib(),
                                          'matplotlib')
        
        if os.path.exists(matplotlib_instdir):
            shutil.rmtree(matplotlib_instdir)

    def get_installed_version(self):
        if WIN64:
            return "No numpy on Win64."

        import matplotlib
        return matplotlib.__version__

        
        

