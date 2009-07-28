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
FILE = "file"

# end of programmes ###############################################

import config
import getopt
import os
import re
import sys
import shutil
import tarfile
import utils

PPF = "[*** DRE build installer ***]"
S_PPF = "%s =====>>>" % (PPF,) # used for stage headers

class BDIPaths:
    dre_basename = None
    dre_dest = None


def copy_inst_to_dre():
    """Copy the dre top-level dir (inst) to final 'dre' 
    """

    print S_PPF, 'Copying INST to DRE.'

    if os.path.isdir(BDIPaths.dre_dest):
        print PPF, 'DRE dir already present.  Skipping step.'
        return

    print PPF, 'Working ...'

    # using ignore callback to give progress
    def _logpath(path, names):
        # would be better to print only if the top-level dir within
        # config.inst_dir changes...
        print "Copying %s." % (path,)
        return []

    # copy symlinks as symlinks!
    shutil.copytree(config.inst_dir, BDIPaths.dre_dest, 
            symlinks=True, ignore=_logpath)

    print PPF, 'DONE copying INST to DRE.'

def postproc_sos():
    if os.name != 'posix':
        return

    print S_PPF, "postproc_sos (strip, chrpath)"

    res = re.compile(
    "^(.*):.*ELF.*(executable|relocatable|shared object).*, not stripped"
    )
    rec = re.compile('.*\.(so$|so\.)')

    # use 'file' command to find all strippable files
    print PPF, "Creating complete file list..."
    all_files, _ = utils.find_files(BDIPaths.dre_dest, '.*')

    print PPF, "Searching for strippable / chrpathable files"
    for f in all_files:
        status, output = utils.get_status_output('%s %s' % (FILE, f))
        mo = re.match(res, output)
        stripped = chrpathed = False
        if mo:
            sfn = mo.groups()[0]
            ret = os.system('%s %s' % (STRIP, sfn))
            if ret != 0:
                print "Error stripping %s." % (sfn,)
            else:
                stripped = True

        # now check if f can be chrpathed
        if re.match(rec, f):
            # remove rpath information
            ret = os.system('%s --delete %s' % (CHRPATH, f))
            if ret != 0:
                print "Error chrpathing %s." % (f,)
            else:
                chrpathed = True

        if stripped or chrpathed:
            actions = [] 
            if stripped:
                actions.append('STRIPPED')
            if chrpathed:
                actions.append('CHRPATHED')
            
            print "%s: %s" % (f, ','.join(actions))

def rebase_dlls(md_paths):
    """Rebase all DLLs in the distdevide tree on Windows.
    """

    if os.name == 'nt':
        print S_PPF, "rebase_dlls"

        # sqlite3.dll cannot be rebased; it even gets corrupted in the
        # process!  see this test:
        # C:\TEMP>rebase -b 0x60000000 -e 0x1000000 sqlite3.dll
        # REBASE: *** RelocateImage failed (sqlite3.dll).  
        # Image may be corrupted

        # get list of pyd / dll files, excluding sqlite3
        so_files, excluded_files = find_files(
                BDIPaths.dre_dest, '.*\.(pyd|dll)', ['sqlite3\.dll'])
        # add newline to each and every filename
        so_files = ['%s\n' % (i,) for i in so_files]

        print "Found %d DLL PYD files..." % (len(so_files),)
        print "Excluded %d files..." % (len(excluded_files),)

        # open file in specfile_dir, write the whole list
        dll_list_fn = os.path.join(
                BDIPaths.dre_dest, 'dll_list.txt')
        dll_list = file(dll_list_fn, 'w')
        dll_list.writelines(so_files)
        dll_list.close()

        # now run rebase on the list
        os.chdir(BDIPaths.dre_dest)
        ret = os.system(
                '%s -b 0x60000000 -e 0x1000000 @dll_list.txt -v' %
                (REBASE,))

        # rebase returns 99 after rebasing, no idea why.
        if ret != 99:
            raise RuntimeError('Could not rebase DLLs.')

def package_dist():
    """4. package and timestamp distributables (nsis on win, tar on
    posix)
    """

    print S_PPF, "package_dist"

    # get devide version (we need this to stamp the executables)
    cmd = '%s -v' % (os.path.join(BDIPaths.dre_dest, 'dre devide'),)
    s,o = utils.get_status_output(cmd)
   
    # s == None if DeVIDE has executed successfully
    if s: 
        raise RuntimeError('Could not exec DeVIDE to extract version.')

    mo = re.search('^DeVIDE\s+(v.*)$', o, re.MULTILINE)
    if mo:
        devide_ver = mo.groups()[0]
    else:
        raise RuntimeError('Could not extract DeVIDE version.')

    if os.name == 'nt':
        # we need to be in the installer directory before starting
        # makensis
        os.chdir(md_paths.specfile_dir)
        cmd = '%s devide.nsi' % (MAKE_NSIS,)
        ret = os.system(cmd)
        if ret != 0:
            raise RuntimeError('Error running NSIS.')

        # nsis creates devidesetup.exe - we're going to rename
        os.rename('devidesetup.exe', 
                'devidesetup-%s.exe' % (devide_ver,))

    else:
        # go to the installer dir
        os.chdir(config.working_dir)

        # rename distdevide to devide-version
        basename = '%s-%s' % (BDIPaths.dre_basename, devide_ver)
        tarball = '%s.tar.bz2' % (basename,)

        if os.path.exists(tarball):
            print PPF, '%s exists, not repacking.' % (tarball,)
            return

        print PPF, 'Packing %s' % (tarball,)

        os.rename(BDIPaths.dre_basename, basename)

        # create tarball with juicy stuff
        tar = tarfile.open(tarball, 'w:bz2')
        # recursively add directory
        tar.add(basename)
        # finalize
        tar.close()

        # rename devide-version back to distdevide
        os.rename(basename, BDIPaths.dre_basename)

        print PPF, 'DONE.'

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
    BDIPaths.dre_basename = 'devide-re'
    BDIPaths.dre_dest = os.path.join(
            config.working_dir, BDIPaths.dre_basename)


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
    if os.name == 'nt':
        rebase_dlls()
    elif os.name == 'posix':
        postproc_sos()


    # 3. posix: tar her up
    #    nt: nsis
    package_dist()


if __name__ == '__main__':
    main()


