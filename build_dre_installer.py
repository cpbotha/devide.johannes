# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

###################################################################
# the following programmes should either be on your path, or you
# should specify the full paths here.

# Microsoft utility to rebase files.
REBASE = "rebase"
MAKE_NSIS = "makensis"

STRIP = "strip"
CHRPATH = "chrpath"

# end of programmes ###############################################

import config
import getopt
import os
import sys
import shutil
import tarfile
import utils

PPF = "[*** DRE build installer ***]"
S_PPF = "%s =====>>>" % (PPF,) # used for stage headers

class BDIPaths:
    dre_dest = None


def copy_inst_to_dre():
    """Copy the dre top-level dir (inst) to final 'dre' 
    """

    print S_PPF, 'Copying INST to DRE.'

    if os.path.isdir(BDIPaths.dre_dest):
        print PPF, 'DRE dir already present.  Skipping step.'
        return

    print PPF, 'Working ...'
    shutil.copytree(config.inst_dir, BDIPaths.dre_dest)
    print 'DONE'


def posix_prereq_check():
    print S_PPF, 'POSIX prereq check'

    # gnu
    # have the word version anywhere
    v = utils.find_command_with_ver(
            'strip',
            '%s --version' % (STRIP,),
            '([0-9\.]+)')

    v = v and utils.find_command_with_ver(
            'chrpath',
            '%s --version' % (CHRPATH,),
            'version\s+([0-9\.]+)')

    return v

def windows_prereq_check():
    print S_PPF, 'WINDOWS prereq check'

    # if you give rebase any other command-line switches (even /?) it
    # exits with return code 99 and outputs its stuff to stderr
    # with -b it exits with return code 0 (expected) and uses stdout
    v = utils.find_command_with_ver(
            'Microsoft Rebase (rebase.exe)', 
            '%s -b 0x60000000' % (REBASE,),
            '^(REBASE):\s+Total.*$')

    v = v and utils.find_command_with_ver(
            'Nullsoft Installer System (makensis.exe)', 
            '%s /version' % (MAKE_NSIS,),
            '^(v[0-9\.]+)$')

    # now check that setuptools is NOT installed (it screws up
    # everything on Windows)
    try:
        import setuptools
    except ImportError:
        # this is what we want
        print PPF, 'setuptools not found. Good!'
        sut_v = True
    else:
        print PPF, """setuptools is installed.

setuptools will break the DeVIDE dist build.  Please uninstall by doing:
\Python25\Scripts\easy_install -m setuptools
del \Python25\Lib\site-packages\setuptools*.*
You can reinstall later by using ez_setup.py again.
"""
        sut_v = False

    return v and sut_v



def usage():
    print "Yo.  HELP."

def main():
    if len(sys.argv) < 2:
        usage()
        return

    try:
        optlist, args = getopt.getopt(
            sys.argv[1:], 'w:',
            ['working-dir='])

    except getopt.GetoptError,e:
        usage()
        return

    working_dir = None
    for o, a in optlist:
        if o in ('-h', '--help'):
            usage()
            return

        if o in ('-w', '--working-dir'):
            working_dir = a


    if working_dir is None:
        usage()
        return
   
    config.init(working_dir, the_profile='default')
    BDIPaths.dre_dest = os.path.join(config.working_dir, 'dre')


    # dependency checking
    if os.name == 'nt':
        if not windows_prereq_check():
            print PPF, "ERR: Windows prerequisites do not check out."
            return 1

    else:
        if not posix_prereq_check():
            print PPF, "ERR: POSIX prerequisites do not check out."
            return 1


    # 1. copy the whole inst dir to 'devide'
    copy_inst_to_dre()
    # 2. posix: strip / chrpath 
    #    nt: rebase
    # 3. posix: tar her up
    #    nt: nsis







if __name__ == '__main__':
    main()


