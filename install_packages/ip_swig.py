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

dependencies = []

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
        # on posix, we have to unpack in the build directory as we're
        # actually going to compile.  On Windows, we unpack binaries
        # in the install step.
        if os.name == "posix":
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
        # these always have to be set, no matter what
        config.SWIG_DIR = self.inst_dir
        if os.name == 'nt':
            ENAME = 'swig.exe'
        else:
            ENAME = 'bin/swig'

        config.SWIG_EXECUTABLE = os.path.join(self.inst_dir, ENAME)

        # now check if the installation needs to be done
        if os.path.exists(self.inst_dir):
            utils.output(
            'SWIG installation directory exists.  Skipping step.')
            return

        if os.name == 'nt':
            # on windows, we simply unpack into the installation dir
            utils.unpack_inst(self.archive_path)
        else:
            # on posix, we have to do a make install
            os.chdir(self.build_dir)
            ret = utils.make_command(None, install=True) 


    def clean_build(self):
        # nuke the build dir, the source dir is pristine and there is
        # no installation
        utils.output("Removing build dir.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

    def get_installed_version(self):
        import re
        ver_re = '^.*Version\s+(.*)$'

        def get_version_from_output(output):
            mo = re.search(ver_re, output, re.MULTILINE)
            if mo:
                version = mo.groups()[0]
            else:
                version = '<Unable to extract version.>'

            return version

        if os.name == 'nt':
            local_path = os.path.join(self.inst_dir, 'swig.exe')
        else:
            local_path = os.path.join(self.inst_dir, 'bin', 'swig')

        if os.path.exists(local_path):
            status,output = utils.get_status_output('%s -version' %
                    (local_path,))

            if status is None:
                version = get_version_from_output(output)
                return 'Locally installed version %s' % (version.strip(),)

        status,output = utils.get_status_output('swig -version')
        if status is None:
            version = get_version_from_output(output)
            return 'System installed version %s' % (version.strip(),)

        return 'Not found.'

