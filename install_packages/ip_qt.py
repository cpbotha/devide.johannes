import config
from install_package import InstallPackage
import os
import shutil
import utils

VERSION = "4.7.4"
BASENAME = "qt"

if os.name == "nt":
    ARCHIVE_BASENAME = "%s-everywhere-opensource-src-%s" % (BASENAME, VERSION)
    ARCHIVE_NAME = "%s.zip" % (ARCHIVE_BASENAME,)
else:
    ARCHIVE_BASENAME = "%s-everywhere-opensource-src-%s" % (BASENAME, VERSION)
    ARCHIVE_NAME = "%s.tar.gz" % (ARCHIVE_BASENAME,)

URL = "http://get.qt.nokia.com/qt/source/%s" % (ARCHIVE_NAME,)

dependencies = []

class Qt(InstallPackage):
    
    def __init__(self):
        self.archive_path = os.path.join(
                config.archive_dir, ARCHIVE_NAME)
        
        self.build_dir = os.path.join(config.build_dir, '%s-%s' %
                                      (BASENAME,VERSION))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)
        
        config.QT_DIR = self.build_dir
        config.QT_BUILD_BIN = os.path.join(self.build_dir, 'bin')
        config.QT_BIN = os.path.join(self.inst_dir, 'bin')

    def get(self):
        if os.path.exists(self.archive_path):
            utils.output("%s already present, skipping step." % BASENAME)
            return
        
        utils.goto_archive()
        utils.urlget(URL)
        
    def unpack(self):
        if os.path.exists(os.path.join(self.build_dir, "configure.exe")):
            utils.output("%s already unpacked. Skipping." % BASENAME)
            return
        
        utils.output("Unpacking %s." % BASENAME)
        utils.unpack_build(self.archive_path)
        
        # Rename the folder:
        shutil.move(os.path.join(config.build_dir, ARCHIVE_BASENAME), 
                    self.build_dir)
        
        
    def configure(self):
        if os.path.exists(os.path.join(self.build_dir, 'Makefile')):
            utils.output("%s build already configured." % BASENAME)
            return
        
        os.chdir(self.build_dir)
        pre_commands = 'SET PATH=%s;%%PATH%% &SET QTDIR=%s' % (
                    config.QT_BIN, # Note: for some reason we must 
                                   # modify the PATH before applying
                                   # the Visual Studio environment, 
                                   # or nmake will not be on the PATH 
                    config.QT_DIR)
        post_commands = 'configure -platform win32-msvc2008'
        communicate = 'o\ny\n' # Select open-source, say yes to agree
        ret = utils.execute_in_vs_environment(post_commands, pre_commands,
                                              communicate)
        
        if ret != 0:
            utils.error("Could not configure %s.  Fix and try again." % BASENAME)
        
        
    def build(self):
        posix_file = os.path.join(config.QT_BUILD_BIN, 'libQtCore4.so') #TODO:
        nt_file = os.path.join(config.QT_BUILD_BIN, 'QtCore4.dll')
        if utils.file_exists(posix_file, nt_file):    
            utils.output("%s already built.  Skipping build step." % BASENAME)
            return
        
        os.chdir(self.build_dir)
        ret = utils.execute_in_vs_environment('nmake')
        
        if ret != 0:
            utils.error("Could not build %s.  Fix and try again." % BASENAME)
        
        
    def install(self):
        if os.path.exists(config.QT_BIN):
            utils.output("%s already installed. Skipping step." % BASENAME)
            return
        
        # Just copy the bin folder
        shutil.copytree(config.QT_BUILD_BIN, config.QT_BIN)
    
    def get_installed_version(self):
        # This only works when PyQt is installed
        import qt 
        return qt.qVersion()
