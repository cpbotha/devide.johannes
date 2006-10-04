import config
import os
import utils
import sys
from install_package import InstallPackage
import utils

WXP_TARBALL = "wxPython-src-2.6.3.3.tar.bz2"
WXP_DIRBASE = WXP_TARBALL[0:WXP_TARBALL.find('tar.bz2')-1]
WXP_URL = "http://surfnet.dl.sourceforge.net/sourceforge/wxpython/%s" % \
          (WXP_TARBALL,)

class WXPython(InstallPackage):

    def __init__(self):
        self.tbfilename = os.path.join(config.archive_dir, WXP_TARBALL)
        self.build_dir = os.path.join(config.build_dir, WXP_DIRBASE)

    def get(self):
        if os.path.exists(self.tbfilename):
            utils.output("%s already present, not downloading." %
                         (WXP_TARBALL,))

        else:
            utils.goto_archive()
            utils.urlget(WXP_URL)

    def unpack(self):
        if os.path.isdir(self.build_dir):
            utils.output("wxPython already unpacked, not redoing.")
        else:
            utils.unpack_build(self.tbfilename)

    def configure(self):
        pass

    def build_and_install_wxwidgets():
        os.chdir(self.build_dir)

        if not os.path.isdir('bld'):
            os.mkdir('bld')
        
        os.chdir('bld')

        ret = os.system('../configure --prefix=%s --with-gtk --with-opengl '
                        '--enable-unicode' %
                        (os.path.join(config.inst_dir,'wx'),))
        if ret != 0:
            raise RuntimeError(
                '##### Error configuring wxWidgets.  Fix and try again.')

        ret = os.system('make install')
        if ret != 0:
            raise RuntimeError(
                '##### Error making wxWidgets.  Fix and try again.')
    
        ret = os.system('make -C contrib/src/animate install')
        if ret != 0:
            raise RuntimeError(
                '##### Error making wxWidgets ANIMATE.  Fix and try again.')
    
        ret = os.system('make -C contrib/src/gizmos install')
        if ret != 0:
            raise RuntimeError(
                '##### Error making wxWidgets GIZMOS.  Fix and try again.')

        ret = os.system('make -C contrib/src/stc install')
        if ret != 0:
            raise RuntimeError(
                '##### Error making wxWidgets STC.  Fix and try again.')

        
    def build(self):
        os.chdir(self.build_dir)

        if os.path.exists(os.path.join(config.inst_dir, 'wx/bin/wx-config')):
            utils.output("wxwidgets already built and installed.")

        else:
            utils.output("Building wxWidgets.")
            self.build_and_install_wxwidgets()

        utils.output("Building wxPython.")
        os.chdir(os.path.join(self.build_dir, 'wxPython'))
        
    def install(self):
        pass


