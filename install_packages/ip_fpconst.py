import config
from install_package import InstallPackage
import os
import shutil
import utils
from subprocess import call

VERSION = "0.7.2"
BASENAME = "fpconst"
SVN_REPO = \
        "http://devide.googlecode.com/svn/trunk/johannes-extra/fpconst-cvp"

dependencies = []

class FPConst(InstallPackage):
    
    def __init__(self):
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
        if os.path.exists(os.path.join(self.site_packages, 'fpconst.py')):
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
        import fpconst
        return fpconst.__version__
