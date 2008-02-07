# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import re
import shutil
import utils

if os.name == 'nt':
    DCMTK_ARCHIVE = "dcmtk-3.5.4.zip"
else:
    DCMTK_ARCHIVE = "dcmtk-3.5.4.tar.gz"

DCMTK_URL = "ftp://dicom.offis.de/pub/dicom/offis/software/dcmtk/" \
            "dcmtk354/%s" % (DCMTK_ARCHIVE,)
DCMTK_DIRBASE = "dcmtk-3.5.4"

class DCMTK(InstallPackage):
    """This is not the best example of a johannes install package.  In
    fact, it's probably the worst example, mostly because DCMTK builds
    like crap.  autoconf on unix, cmake on windows, what's up with
    that?

    In anycase, it works.  Please just ignore it and let it do its
    job.
    """

    def __init__(self):
        self.tbfilename = os.path.join(config.archive_dir,
                DCMTK_ARCHIVE)
        self.build_dir = os.path.join(config.build_dir, DCMTK_DIRBASE)
        self.source_dir = self.build_dir
        self.inst_dir = os.path.join(config.inst_dir, 'dcmtk')

    def get(self):
        if os.path.exists(self.tbfilename):
            utils.output("%s already present, not downloading." %
                         (DCMTK_ARCHIVE,))
        else:
            utils.goto_archive()
            utils.urlget(DCMTK_URL)

    def unpack(self):
        if os.path.isdir(self.build_dir):
            utils.output("DCMTK source already unpacked, not redoing.")
        else:
            utils.output("Unpacking DCMTK source.")
            utils.unpack_build(self.tbfilename)

    def configure_posix(self):
        os.chdir(self.build_dir)
        
        if os.path.exists("dcmdata/config.log"):
            utils.output("DCMTK already configured.  Not redoing.")
        else:
            # we need to configure this without zlib, otherwise dcmtk
            # complains (at least on this system) about the symbol
            # inflateEnd not being available.
            ret = os.system('./configure --without-zlib '
                            '--prefix=%s' % \
                            (self.inst_dir,))
            if ret != 0:
                utils.error('Could not configure dcmtk.  Fix and try again.')
                
            # now modify the generated config/Makefile.def to enable
            # building shared libraries as per
            # http://forum.dcmtk.org/viewtopic.php?t=19
            repls = [('(^CFLAGS\s*=\s*)-O', '\\1-fPIC -O2'),
                     ('(^CXXFLAGS\s*=\s*)-O', '\\1-fPIC -O2'),
                     ('(^AR\s*=\s*)ar', '\\1gcc'),
                     ('(^ARFLAGS\s*=\s*)cruv', '\\1-shared -o'),
                     ('(^LIBEXT\s*=\s*)a', '\\1so'),
                     ('(^RANLIB\s*=\s*)ranlib', '\\1:')]

            utils.re_sub_filter_file(repls, 'config/Makefile.def')


    def configure_nt(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'CMakeFiles/cmake.check_cache')):
            utils.output("DCMTK build already configured.")
            return

        # modify CMakeLists, changing occurrences of /MT into /MD and
        # /MTd into /MDd
        os.chdir(self.build_dir)
        repls = [('\/MT', '/MD')]
        utils.re_sub_filter_file(repls, 'CMakeLists.txt') 

        # then run cmake
        cmake_params = "-DCMAKE_INSTALL_PREFIX=%s " % (self.inst_dir,)
        ret = utils.cmake_command(self.build_dir, self.source_dir,
                cmake_params)

        if ret != 0:
            utils.error("Could not configure DCMTK.  Fix and try again.")

    def configure(self):
        if os.name == 'nt':
            self.configure_nt()
        else:
            self.configure_posix()

    def build_nt(self):
        os.chdir(self.build_dir)
        # do check for some file

        if os.path.exists(os.path.join('dcmdata/libsrc',
            config.BUILD_TARGET, 'dcmdata.lib')):
            utils.output('dcmtk::dcmdata already built.  Skipping.')

        else:
            ret = utils.make_command('dcmtk.sln', install=False,
                    project='dcmdata')

            if ret != 0:
                utils.error('Could not build dcmtk::dcmdata.')

        if os.path.exists(os.path.join('ofstd/libsrc',
            config.BUILD_TARGET, 'ofstd.lib')):
            utils.output('dcmtk::ofstd already built.  Skipping.')

        else:
            ret = utils.make_command('dcmtk.sln', install=False,
                    project='ofstd')

            if ret != 0:
                utils.error('Could not build dcmtk::ofstd.')


    def build_posix(self):
        os.chdir(self.build_dir)
        if os.path.exists("dcmdata/libsrc/libdcmdata.so"):
            utils.output("DCMTK already built. Skipping.")

        else:
            # some machines (read: amsterdam) set an ARCH env variable
            # and this is integrated in the compile invocation, breaking
            # it
            os.environ['ARCH'] = ''

            ret = os.system('make all')
            if ret != 0:
                utils.error('Could not build dcmtk.  Fix and try again.')

    def build(self):
        if os.name == 'nt':
            self.build_nt()
        else:
            self.build_posix()

    def install_nt(self):
        if os.path.exists(self.inst_dir):
            utils.output("DCMTK already installed. Skipping.")

        else:
            # we have to be in the build_dir
            os.chdir(self.build_dir)

            lib_dir = os.path.join(self.inst_dir, 'lib')
            inc_dir = os.path.join(self.inst_dir, 'include', 'dcmtk')
            os.makedirs(lib_dir)
            os.makedirs(inc_dir)

            for modname in ['dcmdata', 'ofstd']:
                lib_src_fn = os.path.join('%s/libsrc' % (modname,), 
                    config.BUILD_TARGET, '%s.lib' % (modname,))
                lib_dst_fn = os.path.join(lib_dir, 
                        '%s.lib' % (modname,))

                shutil.copyfile(lib_src_fn, lib_dst_fn)

            for modname in ['dcmdata', 'ofstd', 'config']:
                inc_src_dir = os.path.join(modname, 'include',
                        'dcmtk', modname)
                inc_dst_dir = os.path.join(inc_dir, modname)
                shutil.copytree(inc_src_dir, inc_dst_dir)

    def install_posix(self):
        if os.path.exists(self.inst_dir):
            utils.output("DCMTK already installed. Skipping.")

        else:
            # some machines (read: amsterdam) set an ARCH env variable
            # and this is integrated in the compile invocation, breaking
            # it
            os.environ['ARCH'] = ''
            
            ret = os.system('make install')
            if ret != 0:
                utils.error('DCMTK make install failed.  Fix and try again.')

            ret = os.system('make install-lib')
            if ret != 0:
                utils.error(
                    'DCMTK make install-lib failed.  Fix and try again.')



    def install(self):
        if os.name == 'nt':
            self.install_nt()
        else:
            self.install_posix()

        # either way, we have to register our binary path with config
        config.DCMTK_INCLUDE = os.path.join(self.inst_dir, 'include')
        config.DCMTK_LIB = os.path.join(self.inst_dir, 'lib')

    def clean_build(self):
        # nuke installation and build directories, at the next run this
        # will lead to a configure, build and install.
        utils.output("Removing DCMTK build and installation dirs.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)
