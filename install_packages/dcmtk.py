import config
from install_package import InstallPackage
import os
import utils

DCMTK_TARBALL = "dcmtk-3.5.4.tar.gz"
DCMTK_URL = "ftp://dicom.offis.de/pub/dicom/offis/software/dcmtk/" \
            "dcmtk354/%s" % (DCMTK_TARBALL,)
DCMTK_DIRBASE = "dcmtk-3.5.4"

class DCMTK(InstallPackage):
    
    def __init__(self):
        self.tbfilename = os.path.join(config.archive_dir, DCMTK_TARBALL)
        self.build_dir = os.path.join(config.build_dir, DCMTK_DIRBASE)
        self.inst_dir = os.path.join(config.inst_dir, 'dcmtk')

    def get(self):
        if os.path.exists(self.tbfilename):
            utils.output("%s already present, not downloading." %
                         (DCMTK_TARBALL,))
        else:
            utils.goto_archive()
            utils.urlget(DCMTK_URL)

    def unpack(self):
        if os.path.isdir(self.build_dir):
            utils.output("DCMTK source already unpacked, not redoing.")
        else:
            utils.output("Unpacking DCMTK source.")
            utils.unpack_build(self.tbfilename)

    def configure(self):
        os.chdir(self.build_dir)
        
        if os.path.exists("dcmdata/config.log"):
            utils.output("DCMTK already configured.  Not redoing.")
        else:
            ret = os.system('./configure --prefix=%s' % (self.inst_dir,))
            if ret != 0:
                utils.error('Could not configure dcmtk.  Fix and try again.')

    def build(self):
        os.chdir(self.build_dir)
        if os.path.exists("dcmdata/libsrc/libdcmdata.a"):
            utils.output("DCMTK already built. Skipping.")

        else:
            ret = os.system('make all')
            if ret != 0:
                utils.error('Could not build dcmtk.  Fix and try again.')

    def install(self):
        if os.path.exists(self.inst_dir):
            utils.output("DCMTK already installed. Skipping.")

        else:
            ret = os.system('make install')
            if ret != 0:
                utils.error('DCMTK make install failed.  Fix and try again.')

            ret = os.system('make install-lib')
            if ret != 0:
                utils.error(
                    'DCMTK make install-lib failed.  Fix and try again.')

                

        # either way, we have to register our binary path with config
        config.DCMTK_INCLUDE = os.path.join(self.inst_dir, 'include')
        config.DCMTK_LIB = os.path.join(self.inst_dir, 'lib')
