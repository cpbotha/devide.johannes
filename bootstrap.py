# python script for bootstrapping the johannes DeVIDE build system
#
# NB:
# 1. on unix systems that don't have Python installed, you should rather
# use bootstrap_stage1.sh and bootstrap_stage2.sh, these are
# shell-based alternatives to bootstrap.py
# 2. on windows systems, you have no choice: you need to have a system
# python installed to run this bootstrap.py script.
# 3. johannes.py will be run by the python that is locally built by
# EITHER bootstrap.py OR bootstrap_stage{1,2}.sh

PYVER_STR = '2.6.2'

import config
import getopt
import os
import stat
import sys
import utils

nt_python = """
@echo off
@rem script to run locally installed johannes python
@rem should be located in johannes wd\jpython.cmd
@rem as it assumes the local install of python is in
@rem wd\inst\python and it's in wd
%~dp0\inst\python\python.exe %1 %2 %3 %4 %5 %6 %7 %8 %9 
"""

posix_python = """
#!/bin/sh
# script to run locally installed johannes python
# should be located in johannes workingdir/jpython.sh
MYDIR=`dirname $0`
export LD_LIBRARY_PATH=$MYDIR/inst/python/lib
export PATH=$MYDIR/inst/python/bin/:\$PATH
python $*
"""


# script to test for presence of required libs on posix
posix_deps_test_c_file = """
#include <bzlib.h>
#include <sqlite3.h>
#include <ncurses.h>
#include <gtk/gtkversion.h>
#include <ft2build.h>
#include <png.h>
#include <zlib.h>
#include <X11/Intrinsic.h>
#include <GL/glu.h>
int main(void) {}
"""

def download_python():
    urlbase = 'http://python.org/ftp/python/%s' % (PYVER_STR,)
    if os.name == 'posix':
        fname = 'Python-%s.tar.bz2' % (PYVER_STR,)
        url = '%s/%s' % (urlbase, fname)
    elif os.name == 'nt':
        import platform
        a = platform.architecture()[0]
        if a == '32bit':
            fname = 'python-%s.msi' % (PYVER_STR,)
            url = '%s/%s' % (urlbase, fname) 
        else:
            fname = 'python-%s.amd64.msi' % (PYVER_STR,)
            url = '%s/%s' % (urlbase, fname)

    utils.goto_archive()
    utils.urlget(url)

    return fname

def usage():
    message = """
Invoke with:
    python bootstrap.py -w working_directory
    """

    print message

def main():
    try:
        optlist, args = getopt.getopt(
                sys.argv[1:], 'w:',
                ['working-dir='])

    except getopt.GetoptError,e:
        usage()
        return

    working_dir = None

    print optlist
    for o, a in optlist:
        if o in ('-w', '--working-dir'):
            working_dir = a

    if not working_dir:
        usage()
        return

    # this will setup the necessary dirs for later calls into utils
    config.init(working_dir, None)

    # first create directory structure
    prepare_dirs(working_dir)

    # now download the python (source for linux, binaries for windows)
    python_fname = download_python()

    if os.name == 'nt':
        # this means we just have to unpack python
        py_msi_dir = os.path.join(config.archive_dir, python_fname)
        py_inst_dir = os.path.join(config.inst_dir, 'python')

        if os.path.exists(py_inst_dir):
            utils.output(
            'Python installation dir present.  Skipping install.')

        else:
            utils.output('Doing local installation of Python.')

            # run with basic interface
            # ret is 0 if successful
            ret = os.system(
                    'msiexec /a %s TARGETDIR=%s /qb' % 
                    (py_msi_dir, py_inst_dir))

            if ret != 0:
                utils.error(
                        'Failed locally installing Python.  EFS / msiexec problems?')

        jpcmd = 'jpython.cmd'
        f = open(os.path.join(config.working_dir, jpcmd), 'w')
        f.write(nt_python)
        f.close()

    else:
        if not posix_deps_test_c():
            print """
JOHANNES ##### cc (compiler) or necessary headers not found.
See error above.  Please fix and try again.

* See the johannes README.txt for more details on which packages to
  install, and also for correct apt-get invocation to install them all
  on for example Debian / Ubuntu.
            """
            return

        if not posix_test_cc():
            utils.output('c++ compiler not found.')
            return

        utils.goto_build()
        tbfn = os.path.join(config.archive_dir, python_fname)
        pybasename = 'Python-%s' % (PYVER_STR,)
        build_dir = os.path.join(config.build_dir, pybasename)

        if not os.path.exists(build_dir):
            utils.unpack(tbfn)

        os.chdir(build_dir)
        ret = os.system(
            './configure --enable-shared --prefix=%s/python' %
            (config.inst_dir,))

        if ret != 0:
            utils.error('Python configure error.')

        # config.MAKE contains -j setting
        # I've had this break with Python 2.6.2, so I'm using straight make here...
        ret = os.system('%s install' % ('make',))
        if ret != 0:
            utils.error('Python build error.')

        # this means we have to test for dependencies and then build
        # Python.
        jpcmd = 'jpython'

        jpcmd_fn = os.path.join(config.working_dir, jpcmd)
        f = open(jpcmd_fn, 'w')
        f.write(posix_python)
        f.close()

        # make it executable
        os.chmod(jpcmd_fn, stat.S_IEXEC)


    print """
######################################################################
Successfully bootstrapped local johannes Python.  Start the full build
system with:
%s johannes.py -w %s
    """ % \
    (os.path.join(config.working_dir, jpcmd), config.working_dir)


def posix_deps_test_c():
    utils.goto_build()
    f = open('dtest.c', 'w')
    f.write(posix_deps_test_c_file)
    f.close()

    ret = os.system(
'cc -I/usr/include/gtk-2.0 -I/usr/include/freetype2 -o dtest dtest.c')

    # True if successful
    return bool(ret == 0)

def posix_test_cc():
    utils.goto_build()
    f = open('cpptest.cc', 'w')
    f.write('int main(void) {}')
    f.close()

    ret = os.system('c++ -o cpptest cpptest.cc')

    # True if successful
    return bool(ret == 0)


def prepare_dirs(working_dir):
    a_dir = os.path.join(working_dir, 'archive')
    b_dir = os.path.join(working_dir, 'build')
    i_dir = os.path.join(working_dir, 'inst')

    for d in [working_dir, a_dir, b_dir, i_dir]:
        if not os.path.exists(d):
            os.mkdir(d)


           

if __name__ == '__main__':
    main()

