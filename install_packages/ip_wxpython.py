# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
import os
import utils
import sys
import shutil
from install_package import InstallPackage
import utils
from distutils import sysconfig

# wxPython 2.8.10.1 had problems building on Linux

WXP_VER = '2.8.9.2'
WXP_URL_BASE = "http://surfnet.dl.sourceforge.net/sourceforge/wxpython/%s"

if os.name == 'posix':
    WXP_ARCHIVE = "wxPython-src-%s.tar.bz2" % (WXP_VER,)
    WXP_DIRBASE = WXP_ARCHIVE[0:WXP_ARCHIVE.find('tar.bz2')-1]    
    WXP_URL = WXP_URL_BASE % (WXP_ARCHIVE,)
elif os.name == 'nt':
    print config.WINARCH
    if config.WINARCH == '32bit':
        WXP_ARCHIVE = "wxPython2.8-win32-unicode-%s-py26.exe" % (WXP_VER,)
    elif config.WINARCH == '64bit':
        WXP_ARCHIVE = "wxPython2.8-win64-unicode-%s-py26.exe" % (WXP_VER,)

    WXP_URL =  WXP_URL_BASE % (WXP_ARCHIVE,)

dependencies = []

class WXPython(InstallPackage):

    def __init__(self):
        self.afilename = os.path.join(config.archive_dir, WXP_ARCHIVE)
        if os.name == 'posix':
            self.build_dir = os.path.join(config.build_dir, WXP_DIRBASE)
            # this is where wxwidgets gets installed on POSIX
            self.inst_dir = os.path.join(config.inst_dir, 'wx')
            # and this is where the wxpython part ends up.
            # python/lib/python2.x/site-packages/
            self.sp_dir = sysconfig.get_python_lib()

    def get(self):
        if os.path.exists(self.afilename):
            utils.output("%s already present, not downloading." %
                         (WXP_ARCHIVE,))

        else:
            utils.goto_archive()
            utils.urlget(WXP_URL)

    def unpack(self):
        if os.name == 'posix':
            if os.path.isdir(self.build_dir):
                utils.output("wxPython already unpacked, not redoing.")
            else:
                utils.unpack_build(self.afilename)

    def configure(self):
        pass

    def build_and_install_wxwidgets(self):
        os.chdir(self.build_dir)

        if not os.path.isdir('bld'):
            os.mkdir('bld')
        
        os.chdir('bld')

        # now we have to fix the IDIOTIC wxWidgets configure; on an FC3
        # machine with openwin on (don't ask, it's amterdam), gl.h is
        # found in /usr/openwin instead of /usr/include.  We prepend
        # /usr/include to this list, we don't care about solaris machines
        # at the moment...
        repls = [('^SEARCH_INCLUDE="\\\\',
                  'SEARCH_INCLUDE="\\\\\n    /usr/include        \\\\')]
        utils.re_sub_filter_file(repls, '../configure')

        ret = os.system('../configure --prefix=%s --with-gtk --with-opengl '
                        '--enable-unicode' %
                        (self.inst_dir,))
        if ret != 0:
            raise RuntimeError(
                '##### Error configuring wxWidgets.  Fix and try again.')

        ret = os.system('make install')
        if ret != 0:
            raise RuntimeError(
                '##### Error making wxWidgets.  Fix and try again.')
    
        ret = os.system('make -C contrib/src/gizmos install')
        if ret != 0:
            raise RuntimeError(
                '##### Error making wxWidgets GIZMOS.  Fix and try again.')

        ret = os.system('make -C contrib/src/stc install')
        if ret != 0:
            raise RuntimeError(
                '##### Error making wxWidgets STC.  Fix and try again.')

    def setup_env_for_wxp_build(self):
        saved = [os.environ.get(key) for key in ['PATH',
            'LD_LIBRARY_PATH', 'PYTHONPATH']]

        # add wx bin to path and wx lib to LD_LIBRARY_PATH
        os.environ['PATH'] = "%s%s%s" % (os.path.join(self.inst_dir, 'bin'),
                                         os.pathsep, os.environ['PATH'])
        os.environ['LD_LIBRARY_PATH'] = "%s%s%s" % \
                                        (os.path.join(self.inst_dir, 'lib'),
                                         os.pathsep,
                                         os.environ.get('LD_LIBRARY_PATH'))
        # we don't want config.py to find an existing build_config.py
        # somewhere else when setup.py runs
        os.environ['PYTHONPATH'] = ''

        return saved

    def restore_env_after_wxp_build(self, saved):
        for idx, key in enumerate(
                ['PATH', 'LD_LIBRARY_PATH', 'PYTHONPATH']):
            if saved[idx] is not None:
                os.environ[key] = saved[idx]

    def build_wxpython(self):

        os.chdir(os.path.join(self.build_dir, 'wxPython'))

        saved = self.setup_env_for_wxp_build()

        # find path to current python binary        
        exe = sys.executable

        ret = os.system(
            '%s setup.py build_ext --inplace UNICODE=1 BUILD_GLCANVAS=1' %
            (exe,))

        self.restore_env_after_wxp_build(saved)
        
        if ret != 0:
            utils.error('wxPython setup failed.  Please fix and try again.')

        
    def build(self):
        if os.name == 'nt':
            utils.output('Not building (WINDOWS).')
            return

        # our build step includes config,build and install of wxwidgets,
        # as this is a dependency of wxPython
        os.chdir(self.build_dir)

        if os.path.exists(os.path.join(config.inst_dir, 'wx/bin/wx-config')):
            utils.output("wxwidgets already built and installed.")

        else:
            utils.output("Building wxWidgets.")
            self.build_and_install_wxwidgets()
            # wxWidgets is now installed to inst_dir/wx

        if os.path.exists(os.path.join(
            self.build_dir, 'wxPython/wx/_core_.so')):
            utils.output("wxPython already built.")
        else:
            # build wxPython now
            utils.output("Building wxPython.")
            self.build_wxpython()

    def install_nt(self):
        if os.path.exists(os.path.join(
            config.PYTHON_SITE_PACKAGES, 'wxversion.py')):
            utils.output('wxPython already installed.')
            return

        utils.goto_archive()
        # innotek installer, run in unattended mode
        cmd = '%s /DIR=%s /sp- /silent /norestart' % \
        (WXP_ARCHIVE, config.PYTHON_SITE_PACKAGES)
        ret = os.system(cmd)
        if ret != 0:
            utils.error('Error install wxPython.')

    def install_posix(self):
        os.chdir(self.build_dir)
        os.chdir('wxPython')

        if os.path.exists(os.path.join(self.sp_dir, 'wxversion.py')):
            utils.output('wxPython already installed.')

        else:
            utils.output('Installing wxPython.')

            saved = self.setup_env_for_wxp_build() 

            # find path to current python binary        
            exe = sys.executable
            ret = os.system(
                '%s setup.py install' % (exe,))

            self.restore_env_after_wxp_build(saved)

            if ret != 0:
                utils.error(
                        'wxPython install failed.  Please fix and try again.')

    def install(self):
        if os.name == 'nt':
            self.install_nt()
        elif os.name == 'posix':
            self.install_posix()

            # LIB_PATH is only used on posix to extend the
            # LD_LIBRARY_PATH.  On Windows this is not necessary
            config.WX_LIB_PATH = os.path.join(self.inst_dir, 'lib')
            # this is where wx-config can be found
            # only valid on posix where matplotlib has to be built
            config.WX_BIN_PATH = os.path.join(self.inst_dir, 'bin')

    def get_installed_version(self):
        import wx
        return wx.VERSION_STRING
        


