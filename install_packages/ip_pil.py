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

dependencies = ['zlib']

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
        
        # 'Manual' editing of setup.py to point to zlib dir
        setup_file = os.path.join(self.build_dir, 'setup.py')
        setup_file_ori = os.path.join(self.build_dir, 'setup_original.py')
        if not os.path.exists(setup_file_ori):
            os.rename(setup_file, setup_file_ori)
        replacement = "'" + config.ZLIB_ROOT + "'"
        replacement = replacement.replace("\\", "\\\\")
        mapping = [['ZLIB_ROOT = *\n', '*', replacement]]
        self.replaceValueInFile(setup_file_ori, setup_file, mapping)
        
        os.chdir(self.build_dir)
        ret = call("%s setup.py build_ext -i" % config.PYTHON_EXECUTABLE, shell=True) 
        
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
    
    def clean_install(self):
        """ Only cleans up the install directory.
        """
        utils.output("Removing installation directory.")
        inst_dir = os.path.join(self.site_packages, 'PIL')
        if os.path.exists(inst_dir):
            shutil.rmtree(inst_dir)
        pilfile = os.path.join(self.site_packages, 'PIL.pth')
        if os.path.exists(pilfile):
            os.remove(pilfile)
        
    def get_installed_version(self):
        import Image
        return Image.VERSION

    def replaceValueInFile(cls, filename_in, filename_out, mappings):
        """ Replaces all values in the input file based on the map
            dictionary and writes the result to a second file.
        """
        file_in = file(filename_in)
        file_out = file(filename_out, 'w')
        
        for line in file_in:
            for mapping in mappings:
                match = mapping[0]
                mask = mapping[1]
                replacement = mapping[2]
                line = cls.replaceValueInString(line, match, mask, replacement)
            file_out.write(line)
            
        file_in.close()
        file_out.close()
    replaceValueInFile = classmethod(replaceValueInFile)
    
    def replaceValueInString(cls, source, match, mask, replacement):
        """ Replaces the value corresponding to the mask 
            in the match string from the source string.
            Example: 
            findValue('parameter=500;next=400', 'parameter=#ANYTHING#;', '#ANYTHING#', '600')
            will replace '500' (the string that corresponds
            to the mask in the match when applied to the source)
            with '600'.
        """
        matches = match.split(mask)
        index1 = source.find(matches[0])
        if index1 >= 0:
            index1 += len(matches[0])
            index2 = source.find(matches[1], index1)
            return source[:index1] + replacement + source[index2:]
        return source
    replaceValueInString = classmethod(replaceValueInString)