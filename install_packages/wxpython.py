import config
import os
import utils
import sys
import shutil
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
        self.inst_dir = os.path.join(config.inst_dir, 'wx')

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
                        (self.inst_dir,))
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

    def build_wxpython(self):
        os.chdir(os.path.join(self.build_dir, 'wxPython'))

        # add wx bin to path and wx lib to LD_LIBRARY_PATH
        os.environ['PATH'] = "%s%s%s" % (os.path.join(self.inst_dir, 'bin'),
                                         os.pathsep, os.environ['PATH'])
        os.environ['LD_LIBRARY_PATH'] = "%s%s%s" % \
                                        (os.path.join(self.inst_dir, 'lib'),
                                         os.pathsep,
                                         os.environ['LD_LIBRARY_PATH'])
        # we don't want config.py to find an existing build_config.py
        # somewhere else when setup.py runs
        os.environ['PYTHONPATH'] = ''

        # find path to current python binary        
        exe = sys.executable

        # fix problem in 2.6.3.3 setup.py
        #inputfile = open('setup.py')
        #outputfile = open('setup_new.py', 'w')
        #for l in inputfile:
        #    if not l.startswith("copy_file('build_options.py'"):
        #        outputfile.write(l)

        #inputfile.close()
        #outputfile.close()
        #shutil.copyfile('setup_new.py','setup.py')
        
        
        ret = os.system('%s setup.py build_ext --inplace UNICODE=1' % (exe,))
        if ret != 0:
            utils.error('wxPython setup failed.  Please fix and try again.')

        
    def build(self):
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

    def install(self):
        os.chdir(self.build_dir)
        os.chdir('wxPython')

        if os.path.exists(os.path.join(self.inst_dir, 'wxPython')):
            utils.output('wxPython already installed.')

        else:
            utils.output('Installing wxPython.')
            shutil.copytree(os.path.join(self.build_dir, 'wxPython'),
                            os.path.join(self.inst_dir, 'wxPython'))
        


