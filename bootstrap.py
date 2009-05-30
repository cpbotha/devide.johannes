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

import config
import getopt
import os
import sys
import utils

nt_python = """
@echo off
@rem script to run locally installed johannes python
@rem should be located in johannes wd\jpython.sh
@rem as it assumes the local install of python is in
@rem wd\inst\python and it's in wd
%~dp0\inst\python\python.exe %1 %2 %3 %4 %5 %6 %7 %8 %9 
"""

def download_python():
    urlbase = 'http://python.org/ftp/python/2.5.4'
    if os.name == 'posix':
        fname = 'Python-2.5.4.tar.bz2'
        url = '%s/%s' % (urlbase, fname)
    elif os.name == 'nt':
        import platform
        a = platform.architecture()[0]
        if a == '32bit':
            fname = 'python-2.5.4.msi'
            url = '%s/%s' % (urlbase, fname) 
        else:
            fname = 'python-2.5.4.amd64.msi'
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
        # this means we have to test for dependencies and then build
        # Python.
        jpcmd = 'jpython.sh'

    print """
Successfully bootstrapped local johannes Python.  Start the full build
system with:
%s johannes.py -w %s
    """ % \
    (os.path.join(config.working_dir, jpcmd), config.working_dir)


def prepare_dirs(working_dir):
    a_dir = os.path.join(working_dir, 'archive')
    b_dir = os.path.join(working_dir, 'build')
    i_dir = os.path.join(working_dir, 'inst')

    for d in [working_dir, a_dir, b_dir, i_dir]:
        if not os.path.exists(d):
            os.mkdir(d)


           

if __name__ == '__main__':
    main()

