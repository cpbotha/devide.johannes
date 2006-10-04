# johannes should be run with a working directory as first parameter
# all packages will be downloaded, configured, built, installed in this dir
# however: a separate install hierarchy can be supplied

import config
import os
import utils
import sys

# turn this into a class, with get, configure, build, install steps
def build_wxwidgets(wx_dir):
    os.chdir(wx_dir)
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

    
def build_wxpython():
    #utils.urlget_and_unpack(config.WXP_URL)

    utils.goto_build()
    wx_dir = os.path.abspath('wxPython-src-2.6.3.3')

    #build_wxwidgets(wx_dir)

    os.chdir(os.path.join(wx_dir, 'wxPython'))

    # inject variables into environment
    # run new python to build wxPython
    

def usage():
    print "johannes working_directory"

def main():
    if len(sys.argv) < 2:
        usage()

    else:
        config.init()
        build_wxpython()

if __name__ == '__main__':
    main()
