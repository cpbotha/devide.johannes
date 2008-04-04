# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import utils
import sys

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

        self.inst_dir = os.path.join(config.inst_dir, ARCHIVE_BASENAME)

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
        if os.name == 'posix':
            os.chdir(self.build_dir)
            if os.path.exists('config.status'):
                utils.output('SWIG already configured, skipping step.')
                return

            configure_command = \
                    "./configure --prefix=%s " \
                    "--with-python=%s " \
                    "--without-tcl --without-perl5 --without-java " \
                    "--without-gcj --without-guile --without-mzscheme " \
                    "--without-ruby --without-php4 --without-ocaml " \
                    "--without-pike --without-chicken --without-csharp " \
                    "--without-lua --without-allegrocl --without-clisp " \
                    "--without-r" % (self.inst_dir, sys.executable)

            ret = os.system(configure_command) 
            if ret != 0:
                utils.error("Could not configure SWIG.  Fix and try again.")
        

    def build(self):
        if os.name == 'posix':
            os.chdir(self.build_dir)
            if os.path.exists('swig'):
                utils.output('SWIG already built.  Skipping step.')
                return

            ret = utils.make_command(None)
            if ret != 0:
                utils.error("Could not build SWIG.  Fix and try again.")

    def install(self):
        config.SWIG_DIR = self.build_dir
        if os.name == 'nt':
            ENAME = 'swig.exe'
        else:
            ENAME = 'swig'

        config.SWIG_EXECUTABLE = os.path.join(self.build_dir, ENAME)
 
    def clean_build(self):
        # nuke the build dir, the source dir is pristine and there is
        # no installation
        utils.output("Removing build dir.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

