import config
from install_package import InstallPackage
import os
import shutil
import utils
from subprocess import call

VERSION = "4.10"
BASENAME = "sip"

if os.name == "nt":
    ARCHIVE_BASENAME = "%s-%s" % (BASENAME, VERSION)
    ARCHIVE_NAME = "%s.zip" % (ARCHIVE_BASENAME,)
else:
    ARCHIVE_BASENAME = "%s-%s" % (BASENAME, VERSION)
    ARCHIVE_NAME = "%s.tar.gz" % (ARCHIVE_BASENAME,)

URL = "http://www.riverbankcomputing.com/static/Downloads/sip4/%s" % (ARCHIVE_NAME,)

dependencies = []

class SIP(InstallPackage):
    
    def __init__(self):
        self.archive_path = os.path.join(
                config.archive_dir, ARCHIVE_NAME)
        
        self.build_dir = os.path.join(config.build_dir, '%s-%s' %
                                      (BASENAME,VERSION))

    def get(self):
        if os.path.exists(self.archive_path):
            utils.output("%s already present, skipping step." % BASENAME)
            return
        
        utils.goto_archive()
        utils.urlget(URL)
        
    def unpack(self):
        if os.path.exists(os.path.join(self.build_dir, "configure.py")):
            utils.output("%s already unpacked. Skipping." % BASENAME)
            return
        
        utils.output("Unpacking %s." % BASENAME)
        utils.unpack_build(self.archive_path)

    def configure(self):
        if os.path.exists(os.path.join(self.build_dir, 'Makefile')):
            utils.output("%s build already configured." % BASENAME)
            return
        
        os.chdir(self.build_dir)
        platform = 'win32-msvc2008' #TODO: platform on linux?
        ret = call('%s configure.py -p %s' %
                (config.PYTHON_EXECUTABLE, platform), shell=True)
        
        if ret != 0:
            utils.error("Could not configure %s.  Fix and try again." % BASENAME)
        
        
    def build(self):
        test_file = os.path.join(self.build_dir, 'sipgen', 'sip.exe')
        if os.path.exists(test_file):
            utils.output("%s already installed, skipping step." % BASENAME)
            return
        
        os.chdir(self.build_dir)
        ret = utils.execute_in_vs_environment('nmake')
        
        if ret != 0:
            utils.error("Could not build %s.  Fix and try again." % BASENAME)
        

    def install(self):
        PYTHON_DIR = os.path.dirname(config.PYTHON_EXECUTABLE)
        test_file = os.path.join(PYTHON_DIR, 'sip.exe')
        if os.path.exists(test_file):
            utils.output("%s already installed, skipping step." % BASENAME)
            return
        
        os.chdir(self.build_dir)
        ret = utils.execute_in_vs_environment('nmake install')
        
        if ret != 0:
            utils.error(
            "Could not install %s.  Fix and try again." % BASENAME)
 
    def clean_build(self):
        # nuke the build dir, the source dir is pristine
        utils.output("Removing build dir.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        # TODO: can we uninstall it?
        
    def get_installed_version(self):
       #TODO: 
        return ""
