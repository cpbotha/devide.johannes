# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.


# for binaries NOT on your PATH, you should specify the complete path here,
# e.g. SVN = '/usr/bin/svn'.  For binaries ON your path, only the binary name
# e.g. SVN = 'svn'

SVN = 'svn'
HG = 'hg'
CVS = 'cvs -z3'
GIT = 'git'
PATCH = 'patch'
# only required on Windows
DEVENV = 'devenv' 
# on windows, cmake should be on your path, or you should specify the
# full path here.  On *ix, you don't have to touch this (johannes
# builds and configures its own cmake)
CMAKE_BINPATH = 'cmake' 

# set to True if you want to use distcc on *ix, False otherwise
HAVE_DISTCC = False
# on *ix, use this many parallel make processes
# if you're using distcc, this should be even higher.
NUM_MAKE_PROCESSES = 4

# Set to True if you want to build redistributable DeVIDE binaries
# with PyInstaller as part of the johannes build process.  If False,
# you can still run DeVIDE directly from its build directory, and you
# can also create redistributable binaries at a later stage.
BUILD_DEVIDE_DISTRIBUTABLES = False

# nothing for you to edit below this line
#######################################################################

import os
import sys

# this is manually updated by the DeVIDE developers to indicate
# which changeset of DeVIDE this johannes changeset is able to build
# FIXME: change devide installpackage to find hg id of the johannes that
# builds it.
DEVIDE_CHANGESET_ID = "5695faaaa814"
# this should be the date of the above changeset ID
# and probably the new-style DeVIDE versioning
# so for release: DeVIDE v11.9.16
# for dev: DeVIDE vDEV11.9.16
DEVIDE_DATESTR = "12.2.7"

DRE_CHANGESET_ID = "b75e1ba9b0a6"
VTKDEVIDE_CHANGESET_ID = "bdc8e1f9e6e6"

BUILD_TARGET = 'RelWithDebInfo'

# will be filled in by init()
JOHANNES_REVISION_ID = "NOT SET"


# the following variables are written by various InstallPackages
####################################################################

# will be written by init()
MAKE = ''
SO_EXT = ''
PYE_EXT = ''

WINARCH = ''
WINARCH_STR = ''

# together with CMAKE_BIN_PATH, these will be used by the utils
# modules to build up a cmake command.
CMAKE_DEFAULT_PARAMS = '' # this will be set by init()
CMAKE_PRE_VARS = ''

DCMTK_INCLUDE = ''
DCMTK_LIB = ''

VTK_DIR = ''
VTK_LIB = ''
VTK_SODIR = ''
VTK_PYTHON = ''

ITK_LIB = ''
ITK_BIN = ''
ITK_PYTHON = ''

GDCM_LIB = ''
GDCM_PYTHON = ''

VTKDEVIDE_LIB = ''
VTKDEVIDE_PYTHON = ''

VTKTUDOSS_LIB = ''
VTKTUDOSS_PYTHON =''

WX_LIB_PATH = ''
WXP_PYTHONPATH = ''

ITK_DIR = ''
ITK_BIN = ''
WRAPITK_LIB = ''
WRAPITK_PYTHON = ''

DEVIDE_PY = ''

PYTHON_EXECUTABLE = ''
PYTHON_INCLUDE_PATH = ''
PYTHON_LIBRARY = ''

DEVIDE_INST_DIR = ''

#######################################################################

# UTILITY method (also available in utils.py which we don't want to import)
def get_status_output(command):
    """Run command, return output of command and exit code in status.
    In general, status is None for success and 1 for command not
    found.
    """

    ph = os.popen(command)
    output = ph.read()
    status = ph.close()
    return (status, output)



def init(wd, the_profile):
    global working_dir, archive_dir, build_dir, inst_dir

    working_dir = os.path.abspath(wd)
    archive_dir = os.path.join(working_dir, 'archive')
    build_dir = os.path.join(working_dir, 'build')
    inst_dir = os.path.join(working_dir, 'inst')


    # we will also need directory where johannes finds itself, in
    # order to retrieve patches.
    global johannes_dir, patches_dir, ip_dir
    johannes_dir = os.path.dirname(__file__)
    patches_dir = os.path.join(johannes_dir, 'patches')
    ip_dir = os.path.join(johannes_dir, 'install_packages')
    
    # get revision ID
    global JOHANNES_REVISION_ID
    status, output = get_status_output("%s id %s" % (HG, johannes_dir))
    # strip is in case we have single token to get rid of \n
    JOHANNES_REVISION_ID = output.split(' ')[0].strip()

    global profile
    profile = the_profile

    global python_library_path, python_binary_path, python_scripts_path
    python_library_path = os.path.join(inst_dir, 'python', 'lib')
    python_binary_path = os.path.join(inst_dir, 'python', 'bin')
    python_scripts_path = os.path.join(inst_dir, 'python', 'Scripts')

    # platform dependent stuff =========================================
    # use conditionals based on os.name (posix, nt) and sys.platform (linux2,
    # win32)

    global MAKE, DEVENV, CMAKE_DEFAULT_PARAMS, CMAKE_PRE_VARS
    global SO_EXT, PYE_EXT
    # FIXME: change convention to x86, amd64, ia64 instead of 32bit and 64bit.
    # Go through all user code to fix.
    global WINARCH, WINARCH_STR

    if os.name == 'posix':
        CMAKE_DEFAULT_PARAMS = '-G "Unix Makefiles"'
        MAKE = 'make -j%d' % (NUM_MAKE_PROCESSES,)

        if HAVE_DISTCC:
            CMAKE_PRE_VARS = 'CC="distcc cc" CXX="distcc c++"'
        else:
            CMAKE_PRE_VARS = ''

        SO_EXT = '.so'
        PYE_EXT = SO_EXT

    elif os.name == 'nt':
        import platform
        a = platform.architecture()[0]
        if a == '32bit':        
            CMAKE_DEFAULT_PARAMS = '-G "Visual Studio 9 2008"'
            # where the %s substitution is the SLN file
            # important that devenv is run, and NOT devenv.exe!
            MAKE = DEVENV + ' %s /project %s ' \
                '/projectconfig "%s|Win32" /build %s'
            WINARCH = '32bit'
            WINARCH_STR = 'x86'

        else:
            CMAKE_DEFAULT_PARAMS = '-G "Visual Studio 9 2008 Win64"'
            # where the %s substitution is the SLN file
            # important that devenv is run, and NOT devenv.exe!
            MAKE = DEVENV + ' %s /project %s ' \
                '/projectconfig "%s|x64" /build %s'
            WINARCH = '64bit'
            WINARCH_STR = 'x64'

        SO_EXT = '.dll'
        PYE_EXT = '.pyd'


    # now setup some python stuff
    global PYTHON_EXECUTABLE
    global PYTHON_INCLUDE_PATH
    global PYTHON_LIBRARY
    global PYTHON_SITE_PACKAGES
    from distutils import sysconfig
    PYTHON_EXECUTABLE = sys.executable 
    PYTHON_INCLUDE_PATH = sysconfig.get_python_inc()
    PYTHON_SITE_PACKAGES = sysconfig.get_python_lib()

    # PYTHON_LIBRARY:
    if os.name == 'posix':
        # under linux, we want the location of libpython2.5.so, under a
        # self-built installation, that's python-inst/lib/libpython2.5.so
        # system installation is /usr/lib/libpython2.5.so
        ldl = sysconfig.get_config_var('LDLIBRARY') # gives the SO name
        ll = os.path.join(sysconfig.get_config_var('prefix'), 'lib')
        PYTHON_LIBRARY = os.path.join(ll, ldl)

    elif os.name == 'nt':
        # under windows, we want Python25\libs\python25.lib (the link
        # stub for the DLL)
        # first derive python25.lib 
        ldl = 'python%s%s.lib' % \
                tuple(sysconfig.get_python_version().split('.')) 
        # then figure out python25\libs
        ll = os.path.join(sysconfig.get_config_var('prefix'), 'libs')
        PYTHON_LIBRARY = os.path.join(ll, ldl)

    if not os.path.exists(PYTHON_LIBRARY):
        raise RuntimeError(
        '!!!!! %s does not exist (python-dev installed?).' %
                (PYTHON_LIBRARY,))




