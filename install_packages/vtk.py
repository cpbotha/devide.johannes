import config
from install_package import InstallPackage
import os
import utils

VTK_TARBALL = "vtk-5.0.2.tar.gz"
VTK_URL = "http://www.vtk.org/files/release/5.0/%s" % (VTK_TARBALL,)
VTK_DIRBASE = "VTK"

class VTK(InstallPackage):
    
    def __init__(self):
        self.tbfilename = os.path.join(config.archive_dir, VTK_TARBALL)
        self.source_dir = os.path.join(config.build_dir, VTK_DIRBASE)
        self.build_dir = os.path.join(config.build_dir, '%s-build' %
                                      (VTK_DIRBASE,))
        self.inst_dir = os.path.join(config.inst_dir, 'VTK')

    def get(self):
        if os.path.exists(self.tbfilename):
            utils.output("%s already present, not downloading." %
                         (VTK_TARBALL,))
        else:
            utils.goto_archive()
            utils.urlget(VTK_URL)

    def unpack(self):
        if os.path.isdir(self.source_dir):
            utils.output("VTK source already unpacked, not redoing.")
        else:
            utils.output("Unpacking VTK source.")
            utils.unpack_build(self.tbfilename)

    def configure(self):
        pass

    def build(self):
        pass

    def install(self):
        pass
        
