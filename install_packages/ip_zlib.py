import config
from install_package import InstallPackage
import os
import shutil
import utils
from subprocess import call

VERSION = "1.2.6"
BASENAME = "zlib"

ARCHIVE_BASENAME = "%s-%s" % (BASENAME, VERSION)
ARCHIVE_NAME = "%s.tar.gz" % (ARCHIVE_BASENAME,)

URL = "http://zlib.net/%s" % (ARCHIVE_NAME,)

dependencies = []

class zlib(InstallPackage):
    """ Not the same as the Python zlib library I guess, but required for PIL.
        Doesn't actually install files; the build folder is used directly
        when building PIL.
    """
    
    def __init__(self):
        self.archive_path = os.path.join(
                config.archive_dir, ARCHIVE_NAME)
        self.build_dir = os.path.join(config.build_dir, '%s-%s' %
                                      (BASENAME,VERSION))
        config.ZLIB_ROOT = self.build_dir
    
    def get(self):
        if os.path.exists(self.archive_path):
            utils.output("%s already present, skipping step." % BASENAME)
            return
        
        utils.goto_archive()
        utils.urlget(URL)
        
    def unpack(self):
        if os.path.exists(self.build_dir):
            utils.output("%s already unpacked. Skipping." % BASENAME)
            return
        
        utils.output("Unpacking %s." % BASENAME)
        utils.unpack_build(self.archive_path)
    
    def build(self):
        if os.path.exists(os.path.join(self.build_dir, 'zlib.h')):
            utils.output("%s already built, skipping step." % BASENAME)
            return
        
        os.chdir(self.build_dir)
        ret = utils.execute_in_vs_environment('nmake /f win32/Makefile.msc')
        
        if ret != 0:
            utils.error("Could not build %s.  Fix and try again." % BASENAME)
        
    def get_installed_version(self):
        return ""
