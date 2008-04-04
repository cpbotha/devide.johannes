# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import utils

SWIG_VER = "1.3.34"
BASENAME = "swig"
BASE_URL = \
        "http://surfnet.dl.sourceforge.net/sourceforge/swig/"

if os.name == "nt":
    ARCHIVE_BASENAME = "%swin-%s" % (BASENAME, SWIG_VER)
    ARCHIVE_NAME = "%s.zip" % (ARCHIVE_BASENAME,)
else:
    ARCHIVE_BASENAME = "%s-%s" % (BASENAME, SWIG_VER)
    ARCHIVE_NAME = "%s.tar.gz" % (ARCHIVE_BASENAME,)

SWIG_URL = BASE_URL + ARCHIVE_NAME

class SWIG(InstallPackage):
    
    def __init__(self):
        self.archive_path = os.path.join(
                config.archive_dir, ARCHIVE_NAME)

        self.build_dir = os.path.join(
                config.build_dir, ARCHIVE_BASENAME)

        self.inst_dir = os.path.join(config.inst_dir, BASENAME)

    def get(self):
        if os.path.exists(self.archive_path):
            utils.output("SWIG already downloaded, skipping step.")

        else:
            utils.goto_archive()
            utils.urlget(SWIG_URL)

    def unpack(self):
        # no unpack step
        if os.path.isdir(self.build_dir):
            utils.output("SWIG already unpacked, skipping step.")

        else:
            utils.output("Unpacking SWIG.")
            utils.unpack_build(self.archive_path)

    def configure(self):
        pass
        

    def build(self):
        pass
        

    def install(self):
        config.SWIG_DIR = self.build_dir
 
    def clean_build(self):
        # nuke the build dir, the source dir is pristine and there is
        # no installation
        utils.output("Removing build dir.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

