import config
from install_package import InstallPackage
import os
import shutil
import utils
from subprocess import call

VERSION = "1.2.7"
BASENAME = "zlib"

ARCHIVE_BASENAME = "%s-%s" % (BASENAME, VERSION)
ZLIB_DIRNAME = ARCHIVE_BASENAME
ARCHIVE_NAME = "%s.tar.gz" % (ARCHIVE_BASENAME,)

URL = "http://zlib.net/%s" % (ARCHIVE_NAME,)

dependencies = []

class zlib(InstallPackage):
    """ Not the same as the Python zlib library I guess, but required for PIL.
        Doesn't actually install files; the build folder is used directly
        when building PIL.
    """
    
    def __init__(self):
        self.archive_path = os.path.join(config.archive_dir, ARCHIVE_NAME)
        self.build_dir = os.path.join(config.build_dir, '%s-%s' % (BASENAME,VERSION))
	self.inst_dir = os.path.join(config.inst_dir, 'zlib')
        config.ZLIB_ROOT = self.build_dir
	config.ZLIB_INST_DIR = self.inst_dir
    
    def get(self):
        if os.path.exists(self.archive_path):
            utils.output("%s already present, skipping step." % BASENAME)
            return
        
        utils.goto_archive()
        utils.urlget(URL)

    def unpack(self):
        if os.name == 'nt':
            utils.output('Skipping unpack (WINDOWS).')
            return

        if os.path.isdir(self.build_dir):
            utils.output("%s source already unpacked, not redoing." % BASENAME)
        else:
            utils.output("Unpacking %s source." % BASENAME)
            utils.unpack_build(self.archive_path)

    def configure(self):
        if os.name == 'nt':
            utils.output('Skipping configure (WINDOWS).')
            return

        os.chdir(self.build_dir)
        
        if os.path.exists("configure.log"):
            utils.output("%s already configured.  Not redoing." % BASENAME)
        else:
            ret = os.system('./configure --prefix=%s' % (self.inst_dir,))
            if ret != 0:
                utils.error('Could not configure %s.  Fix and try again.' % BASENAME)


    def build(self):
        if os.name == 'nt':
            utils.output('Skipping build (WINDOWS).')
            return

        os.chdir(self.build_dir)
        if os.path.exists(os.path.join(self.build_dir, 'minigzip')) or os.path.exists(os.path.join(self.build_dir, 'minigzip.exe')):
            utils.output("%s already built, skipping step." % BASENAME)
        else:
            ret = os.system('make')
            if ret != 0:
                utils.error("Could not build %s.  Fix and try again." % BASENAME)





    def install_nt(self):
        config.CMAKE_BINPATH = os.path.join(self.inst_dir, 'bin', 'libz.dll')


        utils.goto_inst()
        if os.path.exists('libz'):
            utils.output('%s already installed, Skipping.' % BASENAME)
            return

        # this will unpack into inst/cmake-VER-win32-x86/bin etc
        utils.unpack(self.archive_path)
        # so we rename it to plain 'cmake'
        os.rename(ZLIB_DIRBASE, 'libz')

    def install_posix(self):
        libz_binpath = os.path.join(self.inst_dir, 'lib/libz.so')
        if os.path.exists(libz_binpath):
            utils.output("%s already installed. Skipping." % BASENAME)

        else:
            ret = os.system('make install')
            if ret != 0:
                utils.error('Could not install %s.  Fix and try again.' % BASENAME)

        # either way, we have to register our binary path with config
        config.LIBZ_BINPATH = libz_binpath

    def install(self):
        if os.name == 'posix':
            self.install_posix()

        elif os.name == 'nt':
            self.install_nt()

    def clean_build(self):
        utils.output("Removing build and install directories.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)

    def get_installed_version(self):
        version = None
	#use glob and with 'libz.so.*', strip all libz.so. away, leaving the pure version 

        #local_libz_path = os.path.join(self.inst_dir, 'lib', 'libz')
	#posix_path = local_libz_path+".so"
	#nt_path = local_libz_path+".lib"
        #if os.path.exists(posix_path) or os.path.exists(nt_path):
        #    status,output = utils.get_status_output('%s --version' % (local_cmake_path,))

        #    if status is None:
        #        return '%s (local)' % (output.strip(),)

        #status,output = utils.get_status_output('cmake --version')
        #if status is None:
        #    return '%s (system)' % (output.strip(),)

        #return 'Not found.'
