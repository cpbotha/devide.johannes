# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.


# for binaries NOT on your PATH, you should specify the complete path here,
# e.g. SVN = '/usr/bin/svn'.  For binaries ON your path, only the binary name
# e.g. SVN = 'svn'

SVN = 'svn'
CVS = 'cvs -z3'
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
NUM_MAKE_PROCESSES = 2

# Set to True if you want to build redistributable DeVIDE binaries
# with PyInstaller as part of the johannes build process.  If False,
# you can still run DeVIDE directly from its build directory, and you
# can also create redistributable binaries at a later stage.
BUILD_DEVIDE_DISTRIBUTABLES = False

# nothing for you to edit below this line
#######################################################################

import os
import sys

# currently, this is only being used by the devide InstallPackage to
# modify the devide version to include the johannes version used to
# build it, so it is important that you change this timestamp so that
# config.py gets updated with a new revision keyword when you are
# shipping a new devide.
STAMP = "20090203-14:54"
JOHANNES_REV = "$Revision$"
JOHANNES_REL = JOHANNES_REV.split()[1]

# same repo, current johannes should be able to build current devide
DEVIDE_REL = JOHANNES_REL

BUILD_TARGET = 'RelWithDebInfo'


# the following variables are written by various InstallPackages
####################################################################

# will be written by init()
MAKE = ''
SO_EXT = ''
PYE_EXT = ''

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

#######################################################################



def init(wd, the_profile):
    global working_dir, archive_dir, build_dir, inst_dir

    working_dir = os.path.abspath(wd)
    archive_dir = os.path.join(working_dir, 'archive')
    build_dir = os.path.join(working_dir, 'build')
    inst_dir = os.path.join(working_dir, 'inst')


    # we will also need directory where johannes finds itself, in
    # order to retrieve patches.
    global johannes_dir, patches_dir
    johannes_dir = os.path.dirname(__file__)
    patches_dir = os.path.join(johannes_dir, 'patches')

    global profile
    profile = the_profile

    global python_library_path, python_binary_path
    python_library_path = os.path.join(inst_dir, 'python/lib')
    python_binary_path = os.path.join(inst_dir, 'python/bin')

    # platform dependent stuff =========================================
    # use conditionals based on os.name (posix, nt) and sys.platform (linux2,
    # win32)

    global MAKE, DEVENV, CMAKE_DEFAULT_PARAMS, CMAKE_PRE_VARS
    global SO_EXT, PYE_EXT

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
        CMAKE_DEFAULT_PARAMS = '-G "Visual Studio 8 2005"'
        # where the %s substitution is the SLN file
        # important that devenv is run, and NOT devenv.exe!
        MAKE = DEVENV + ' %s /project %s ' \
            '/projectconfig "%s|Win32" /build %s'

        SO_EXT = '.dll'
        PYE_EXT = '.pyd'


    # now setup some python stuff
    global PYTHON_EXECUTABLE
    global PYTHON_INCLUDE_PATH
    global PYTHON_LIBRARY
    from distutils import sysconfig
    PYTHON_EXECUTABLE = sys.executable 
    PYTHON_INCLUDE_PATH = sysconfig.get_python_inc()

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
        raise RuntimeError('!!!!! %s does not exist.' %
                (PYTHON_LIBRARY,))




