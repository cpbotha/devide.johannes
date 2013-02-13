import config
from install_package import InstallPackage
import os
import shutil
import utils
from subprocess import call
import struct

VERSION = "1.3.2"
BASENAME = "Opcode"

ARCHIVE_BASENAME = "%s%s" % (BASENAME, VERSION)
ARCHIVE_NAME = "%s.zip" % (ARCHIVE_BASENAME,)

URL = "http://www.lia.ufc.br/~gilvan/cd/%s" % (ARCHIVE_NAME,)

dependencies = []

# this patch removes all if-then-else constructs that choose between 32-bit ASM and standard C++ code,
# instead removing all the ASM code completely. This enables compilation of 64-bit.
OPCODE_PATCH = "opcode132_x64.diff"

class Opcode(InstallPackage):
    """ This version of Opcode was modified from the official version 1.3 by Gilvan Maia.
        An important addition is that is can also compile on 64-bit. In practice this requires
        removing all code-blocks that contain 32-bit assembly (see the patch in Johannes).
    """
    
    def __init__(self):
        self.archive_path = os.path.join(
                config.archive_dir, ARCHIVE_NAME)
        self.build_dir = os.path.join(config.build_dir, '%s' %
                                      (ARCHIVE_BASENAME,))
        self.opcode_patch_src = os.path.join(config.patches_dir, OPCODE_PATCH)
        self.opcode_patch_dst = os.path.join(self.build_dir, OPCODE_PATCH)                                                      
    
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
        
        os.mkdir(self.build_dir)
        os.chdir(self.build_dir)
                
        utils.output("Unpacking %s." % BASENAME)        
        utils.unpack(os.path.join(self.archive_path))
        
        if ( 8 * struct.calcsize("P") == 32):    #32-bit
            utils.output("Detected 32-bit environment. No code patch necessary.")
        elif ( 8 * struct.calcsize("P") == 64):    #64-bit
            utils.output("Detected 64-bit environment, applying Opcode_x64 patch...")
            # we do this copy so we can see if the patch has been done yet or not
            shutil.copyfile(self.opcode_patch_src, self.opcode_patch_dst)                        
            os.chdir(self.build_dir)
            # we have to strip the leading directory names (included by diff) from the patch filenames, hence the -p1
            ret = os.system(
                "%s -p1 < %s" % (config.PATCH, OPCODE_PATCH))                    
            if ret != 0:
                utils.error("Could not apply Opcode_x64 patch.  Fix and try again.")            
        else:
            utils.error("Could not determine bit depth. %d bit??? Aborting!" % (8 * struct.calcsize("P")))
        
    def build(self):
        print '\n-=-=-=-=-'
        print "WARNING: Opcode cannot currently be automatically built.\nYou'll have to do this manually through Visual Studio (Windows)\n"
        print "Please convert %s\\Opcode_vc8.vcproj to a\n MSVC 9.0 (or newer) project file by opening it manually and converting it with the supplied wizard" % (self.build_dir)
        print '\nYou can then build it manually.'
        print '-=-=-=-=-\n'
                
    def get_installed_version(self):
        return ""