import config
from install_package import InstallPackage
import os
import shutil
import utils
from subprocess import call

VERSION = "1.1.7"
BASENAME = "Imaging"

ARCHIVE_BASENAME = "%s-%s" % (BASENAME, VERSION)
ARCHIVE_NAME = "%s.tar.gz" % (ARCHIVE_BASENAME,)

URL = "http://effbot.org/downloads/%s" % (ARCHIVE_NAME,)

dependencies = []

#TODO: implement clean/uninstall functionality
class PIL(InstallPackage):
    
    def __init__(self):
        self.archive_path = os.path.join(
                config.archive_dir, ARCHIVE_NAME)
        self.build_dir = os.path.join(config.build_dir, '%s-%s' %
                                      (BASENAME,VERSION))
        self.site_packages = os.path.join(config.inst_dir, 'python',
                                          'Lib', 'site-packages')

    def get(self):
        if os.path.exists(self.archive_path):
            utils.output("%s already present, skipping step." % BASENAME)
            return
        
        utils.goto_archive()
        utils.urlget(URL)
        
    def unpack(self):
        if os.path.exists(os.path.join(self.build_dir, 'PIL')):
            utils.output("%s already unpacked. Skipping." % BASENAME)
            return
        
        utils.output("Unpacking %s." % BASENAME)
        utils.unpack_build(self.archive_path)
    
    def build(self):
        if os.path.exists(os.path.join(self.build_dir, 'build')):
            utils.output("%s already built, skipping step." % BASENAME)
            return
        
        os.chdir(self.build_dir)
        ret = call("%s setup.py build" % config.PYTHON_EXECUTABLE, shell=True) 
        
        if ret != 0:
            utils.error("Could not build %s.  Fix and try again." % BASENAME)
            
    def install(self):
        if os.path.exists(os.path.join(self.site_packages, 'PIL')):
            utils.output("%s already installed. Skipping step." % BASENAME)
            return
        
        os.chdir(self.build_dir)
        ret = call("%s setup.py install" % config.PYTHON_EXECUTABLE, shell=True) 
        
        if ret != 0:
            utils.error("Could not install %s.  Fix and try again." % BASENAME)
    
    def get_installed_version(self):
        import Image
        return Image.VERSION
