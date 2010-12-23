import config
from install_package import InstallPackage
import os
import shutil
import utils
from subprocess import call

VERSION = "4.4"
REPO_VERSION = "04_4"
BASENAME = "elastix"
SVN_REPO = "https://svn.bigr.nl/elastix/tagspublic/elastix_%s" % (REPO_VERSION,)

dependencies = ['CMake', 'ITK']

class Elastix(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.archive_dir, '%s' %
                                       (BASENAME,), 'src')
        self.build_dir = os.path.join(config.build_dir, '%s-%s' %
                                      (BASENAME, VERSION))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)

    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("%s already checked out, skipping step." % BASENAME)
            return
        
        os.chdir(config.archive_dir)
        ret = call("%s co --username elastixguest --password elastixguest %s %s" % \
            (config.SVN, SVN_REPO, BASENAME), shell=True)
        if ret != 0:
            utils.error("Could not SVN checkout.  Fix and try again.")

    def unpack(self):
        # no unpack step
        pass

    def configure(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'CMakeFiles/cmake.check_cache')):
            utils.output("%s build already configured." % BASENAME)
            return
        
        if not os.path.exists(self.build_dir):
            os.mkdir(self.build_dir)

        cmake_params = \
                "-DCMAKE_BACKWARDS_COMPATIBILITY=2.6 " \
                "-DCMAKE_BUILD_TYPE=RelWithDebInfo " \
                "-DCMAKE_INSTALL_PREFIX=%s " \
                "-DITK_DIR=%s " % (
                                   self.inst_dir,
                                   config.ITK_DIR)
                
        ret = utils.cmake_command(self.build_dir, self.source_dir,
                cmake_params)

        if ret != 0:
            utils.error("Could not configure %s.  Fix and try again." % BASENAME)
        
        
    def build(self):
        # Do not check for existance of self.build_dir.
        # Visual Studio will only build if out-of-date.
        
        os.chdir(self.build_dir)
        ret = utils.make_command('elastix.sln')
        
        if ret != 0:
            utils.error("Could not build %s.  Fix and try again." % BASENAME)
        
    def install(self):
        if os.path.exists(self.inst_dir):
            utils.output("%s already installed, skipping step." % BASENAME)
            return
        
        os.chdir(self.build_dir)
        ret = utils.make_command('elastix.sln', install=True)
        
        if ret != 0:
            utils.error(
            "Could not install %s.  Fix and try again." % BASENAME)
        
    def clean_build(self):
        utils.output("Removing build and installation directories.")
        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
    
    def clean_install(self):
        utils.output("Removing installation directory.")
        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)
    
    def get_installed_version(self):
        os.chdir(self.inst_dir)
        reader = os.popen('elastix.exe --version')
        version = reader.read()[:-1] # Cut off newline
        reader.close()
        return version
