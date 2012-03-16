import config
from install_package import InstallPackage
import os
import shutil
import utils
from subprocess import call

VERSION = "0_6_9"
BASENAME = "py2exe"

#ARCHIVE_BASENAME = "%s-%s" % (BASENAME, VERSION)
#ARCHIVE_NAME = "%s.zip" % (ARCHIVE_BASENAME,)

SVN_REPO = \
    "https://py2exe.svn.sourceforge.net/svnroot/py2exe/tags/release_%s" % (VERSION,)

#URL = "http://downloads.sourceforge.net/project/py2exe/py2exe/%s/%s?use_mirror=switch" % (VERSION, ARCHIVE_NAME)

dependencies = []

class Py2exe(InstallPackage):
    
    def __init__(self):
        
#        self.archive_path = os.path.join(
#                config.archive_dir, ARCHIVE_NAME)
        self.source_dir = os.path.join(config.archive_dir, BASENAME)
        self.build_dir = os.path.join(config.build_dir, '%s-build' %
                                      (BASENAME,))
        self.site_packages = os.path.join(config.inst_dir, 'python',
                                          'Lib', 'site-packages')

    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("%s already checked out, skipping step." % BASENAME)
            return
        
        os.chdir(config.archive_dir)
        ret = call("%s co %s %s" % (config.SVN,
            SVN_REPO, BASENAME), shell=True)
        
        if ret != 0:
            utils.error("Could not SVN checkout.  Fix and try again.")
        
    def build(self):
        if os.path.exists(self.build_dir):
            utils.output("%s already built, skipping step." % BASENAME)
            return
        
        shutil.copytree(self.source_dir, self.build_dir)
        os.chdir(self.build_dir)
        ret = call("%s setup.py build" % config.PYTHON_EXECUTABLE, shell=True) 
        
        if ret != 0:
            utils.error("Could not build %s.  Fix and try again." % BASENAME)
            
    def install(self):
        if os.path.exists(os.path.join(self.site_packages, 'py2exe')):
            utils.output("%s already installed. Skipping step." % BASENAME)
            return
        
        os.chdir(self.build_dir)
        ret = call("%s setup.py install" % config.PYTHON_EXECUTABLE, shell=True) 
        
        if ret != 0:
            utils.error("Could not install %s.  Fix and try again." % BASENAME)
        
    def clean_build(self):
        # nuke the build dir, the source dir is pristine
        utils.output("Removing build dir.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        # TODO: can we uninstall it?
        
    def get_installed_version(self):
        import py2exe
        return py2exe.__version__
