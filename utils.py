# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
import os
import re
import sys, urllib
import shutil
import tarfile
import zipfile

def cmake_command(build_dir, source_dir, cmake_params):
    """Invoke correct cmake commands to configure a build directory.

    @param build_dir: out-of-source build directory.  method will
    chdir there before invoking cmake
    @param source_dir: location of the source that will be built
    @cmake_params: string of "-Dparam=blaat -Dparam2=blaat" specifying
    cmake parameters
    """

    # first create correct cmake invocation
    cmake = '%s %s' % (config.CMAKE_BINPATH, config.CMAKE_DEFAULT_PARAMS)
    if len(config.CMAKE_PRE_VARS):
        cmake = config.CMAKE_PRE_VARS + ' ' + cmake

    # then go to build_dir
    os.chdir(build_dir)

    # then invoke cmake
    ret = os.system("%s %s %s" %
                    (cmake, cmake_params, source_dir))

    # on windows, we have to do this a second time (first time
    # configures, second time generates)
    if os.name == 'nt':
        ret = os.system("%s %s %s" %
                        (cmake, cmake_params, source_dir))

    return ret

def find_command_with_ver(name, command, ver_re):
    """Try to run command, use ver_re regular expression to parse for
    the version string.  This will print for example:
    CVS: version 2.11 found.

    @return: True if command found, False if not or if version could
    not be parsed. 
    """

    retval = False
    s,o = get_status_output(command)

    if s:
        msg2 = 'NOT FOUND!'

    else:
        mo = re.search(ver_re, o, re.MULTILINE) 
        if mo:
            msg2 = 'version %s found.' % (mo.groups()[0],)
            retval = True
        else:
            msg2 = 'could not extract version.'


    output("%s: %s" % (name, msg2))

    return retval

def get_status_output(command):
    """Run command, return output of command and exit code in status.
    In general, status is None for success and 1 for command not
    found.
    """

    ph = os.popen(command)
    output = ph.read()
    status = ph.close()
    return (status, output)


def output(message, rpad=0, rpad_char='#'):
    s = "#####J> %s" % (message,)
    pn = rpad - len(s)
    if pn < 0:
        pn = 0
    p = pn * rpad_char
        
    print "%s %s" % (s,p)

    # flush the buffer, else things are out of sync in any log files
    sys.stdout.flush()

def error(message):
    raise RuntimeError('!!!!! %s' % (message,))

def file_exists(posix_file, nt_file):
    """Used to perform platform-specific file existence check.
    """

    if os.name == 'posix':
        fn = posix_file
    else: # os.name == 'nt'
        fn = nt_file

    return os.path.exists(fn)

def human_size(num):
    """Method to convert number of bytes to human-readable version.
    Code from http://blogmag.net/blog/read/38/Print_human_readable_file_size
    """

    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0

def make_command(solution_file, install=False, project=None,
        win_buildtype=None):
    """Install packages can use this method to invoke the
    platform-specific compile command.  This can only be run after
    config.init() has run.

    @param solution_file: only used on Windows, ignored on *ix.
    @param install: if true, invokes the make command to install the
    built project.
    @param project: Only build the named project on Windows.  This
    overrides the install setting!  
    @param win_buildtype: change the buildtype on windows, default
    value is None, which gets translated to the value of
    config.BUILD_TARGET. 
    """

    if os.name == 'posix':
        if install:
            make_command = '%s install' % (config.MAKE,)
        else:
            make_command = config.MAKE

    else: # os.name == 'nt'
        if install:
            prj = 'INSTALL'
        else:
            prj = 'ALL_BUILD'

        if project:
            prj = project

        if win_buildtype:
            buildtype = win_buildtype
        else:
            buildtype = config.BUILD_TARGET

        make_command = config.MAKE % \
            (solution_file, prj, buildtype, buildtype)

    return os.system(make_command)

def urlget(url):
    """Simple method to retrieve URL.  It will get the file in the current
    directory.
    """
    
    def reporthook(blocknum, blocksize, totalsize):
        current_size = blocknum * blocksize
        current_size_kb = int(current_size / 1024.0)
        sys.stdout.write(
            '% 4.0f %% (%d Kbytes) downloaded\r' %
            (current_size / float(totalsize) * 100.0, current_size_kb))

    i = url.rfind('/')
    filename = url[i+1:]
    print url, "->", filename
    if os.path.exists(filename):
        output("%s already present, skipping download." % (filename,))

    else:
        urllib.urlretrieve(url, filename, reporthook)
        sys.stdout.write("\n")
        output("Download complete.")

    return filename


def goto_archive():
    os.chdir(config.archive_dir)

def goto_build():
    os.chdir(config.build_dir)

def unpack_build(archive_filename):
    """Unpack given archive_filename in build directory.
    """

    goto_build()

    tar = None
    zip = None

    if archive_filename.lower().endswith('bz2'):
        m = 'r|bz2'
        tar = tarfile.open(archive_filename, m)

    elif archive_filename.lower().endswith('gz'):
        m = 'r|gz'
        tar = tarfile.open(archive_filename, m)

    else:
        zip = zipfile.ZipFile(archive_filename)

    if tar:
        # extractall is from python 2.5 onwards
        # tar.extractall()
        # we use a form that works on previous versions as well
        for tarinfo in tar:
            print tarinfo.name
            tar.extract(tarinfo)
            
        tar.close()

    else:
        for zipinfo in zip.infolist():

            # first check if we need to create the directory housing
            # the file
            dn = os.path.dirname(zipinfo.filename)
            if dn and not os.path.isdir(dn):
                os.makedirs(dn)

            # we only extract the file if it's not purely a directory
            if not os.path.isdir(zipinfo.filename):
                print "%s - %s" % (zipinfo.filename, \
                                   human_size(zipinfo.file_size))
                # have to write this in binary mode, else we screw up
                # binaries (EXEs and such) quite badly. :)
                f = open(zipinfo.filename, 'wb')
                f.write(zip.read(zipinfo.filename))
                f.close()

        zip.close()

def re_sub_filter_file(repls, filename):
    """Given a list of repls (tuples with regular expresions and
    replacement patterns that are used as the first and second params
    of re.sub), filter filename line by line.

    A backup of the file is made to filename.orig.
    """

    newfilename = '%s.new' % (filename,)
    origfilename = '%s.orig' % (filename,)

    shutil.copyfile(filename, origfilename)

    ifile = file(filename)
    ofile = file(newfilename, 'w')

    for l in ifile:
        for r in repls:
            l = re.sub(r[0], r[1], l)

        ofile.write(l)

    ifile.close()
    ofile.close()
            
    shutil.copyfile(newfilename, filename)
