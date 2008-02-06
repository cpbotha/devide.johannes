import config
from install_package import InstallPackage
import os
import shutil
import sys
import utils

# change this to upgrade the pyinstaller version
INSTALLER_VER = "1.3"

INSTALLER_BASENAME = "pyinstaller"
# directory has dash
INSTALLER_DIRBASE = INSTALLER_BASENAME + "-" + INSTALLER_VER
# archive has underscore
INSTALLER_ARCBASE = INSTALLER_BASENAME + "_" + INSTALLER_VER

if os.name == 'nt':
    INSTALLER_ARCHIVE = INSTALLER_ARCBASE + ".zip"
else:
    INSTALLER_ARCHIVE = INSTALLER_ARCBASE + ".tar.gz"

INSTALLER_URL = "http://pyinstaller.hpcf.upr.edu/source/%s/%s" % \
                (INSTALLER_VER, INSTALLER_ARCHIVE)

class Installer(InstallPackage):

    def __init__(self):
        self.tbfilename = os.path.join(config.archive_dir,
                INSTALLER_ARCHIVE)
        self.build_dir = os.path.join(config.build_dir, INSTALLER_DIRBASE)
        self.inst_dir = os.path.join(config.inst_dir, 'installer')

    def get(self):
        if os.path.exists(self.tbfilename):
            utils.output("%s already present, not downloading." %
                         (INSTALLER_ARCHIVE,))
        else:
            utils.goto_archive()
            utils.urlget(INSTALLER_URL)

    def unpack(self):
        if os.path.isdir(self.build_dir):
            utils.output("INSTALLER source already unpacked, not redoing.")
        else:
            utils.output("Unpacking INSTALLER source.")
            utils.unpack_build(self.tbfilename)
            # and we need to delete the irritating optparse.py from
            # the installer directory (it's only needed for older
            # pythons, and tends to break things in johannes)
            os.unlink(os.path.join(self.build_dir, 'optparse.py'))

    def configure(self):
        pass

    def build_posix_part(self):
        os.chdir(os.path.join('source', 'linux'))

        ret = os.system('%s Make.py' % (sys.executable,))
        if ret != 0:
            utils.error('Error creating make file.  Fix and try again.')

        # on GCCs with ProPolice, the stupid thing thinks that the
        # McMillan installer is trying to smash the stack.
        utils.re_sub_filter_file([("^CFLAGS=(.*)$","CFLAGS=\\1 "
                                   "-fno-stack-protector")],
                                 'Makefile')

        ret = os.system('make')
        if ret != 0:
            utils.error('Could not build stub.  Fix and try again.')

    def build(self):
        os.chdir(self.build_dir)

        # weak test... there are .so files deeper, but they're in platform
        # specific directories
        if os.path.exists('config.dat'):
            utils.output('installer already built.  Skipping step.')

        else:
            if os.name == 'posix':
                self.build_posix_part()

            os.chdir(self.build_dir)
            ret = os.system('%s Configure.py' % (sys.executable,))
            if ret != 0:
                utils.error('Error pre-configuring.  Fix and try again.')

    def install(self):
        # set variables here
        config.INSTALLER_DIR = self.build_dir
        
    def clean_build(self):
        utils.output("Removing build and install directories.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

        
        

