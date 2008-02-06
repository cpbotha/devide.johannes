# for binaries not on your PATH, you should specify the complete path here,
# e.g. SVN = '/usr/bin/svn'.  For binaries ON your path, only the binary name
# e.g. SVN = 'svn'
SVN = 'svn'
CVS = 'cvs -z3'
PATCH = 'patch'

# set to True if you want to use distcc on *ix, False otherwise
HAVE_DISTCC = False 
# on *ix, use this many parallel make processes
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
# build it, so it is important that you change this file (config.py)
# when you prepare a johannes-based release.

JOHANNES_REV = "$Revision$"
JOHANNES_REL = JOHANNES_REV.split()[1]

#DEVIDE_REL = "2482" # check svn log devide for this...
# same repo, current johannes should be able to build current devide
DEVIDE_REL = JOHANNES_REL

# 
ITKTUDOSS_REL = "5"
VTKTUDOSS_REL = "6"

BUILD_TARGET = 'RelWithDebInfo'


# the following variables are written by various InstallPackages
####################################################################

# will be written by init()
MAKE = ''
SO_EXT = ''

# this one will be set by the cmake install package, but we set it to
# a sane default in case the cmake install package is not executed.
CMAKE_BINPATH = 'cmake' 
CMAKE_DEFAULT_PARAMS = '' # this will be set by init()
CMAKE_PRE_VARS = ''

DCMTK_INCLUDE = ''
DCMTK_LIB = ''

VTK_DIR = ''
VTK_LIB = ''
VTK_SODIR = ''
VTK_PYTHON = ''

WX_LIB_PATH = ''
WXP_PYTHONPATH = ''

ITK_DIR = ''
WRAPITK_LIB = ''
WRAPITK_PYTHON = ''

DEVIDE_PY = ''

#######################################################################



def init(wd, the_profile):
    global working_dir, archive_dir, build_dir, inst_dir
    working_dir = os.path.abspath(wd)
    archive_dir = os.path.join(working_dir, 'archive')
    build_dir = os.path.join(working_dir, 'build')
    inst_dir = os.path.join(working_dir, 'inst')

    global profile
    profile = the_profile

    global python_library_path, python_binary_path
    python_library_path = os.path.join(inst_dir, 'python/lib')
    python_binary_path = os.path.join(inst_dir, 'python/bin')

    # platform dependent stuff =========================================
    # use conditionals based on os.name (posix, nt) and sys.platform (linux2,
    # win32)

    global MAKE, CMAKE_DEFAULT_PARAMS, CMAKE_PRE_VARS, SO_EXT

    if os.name == 'posix':
        CMAKE_DEFAULT_PARAMS = '-G "Unix Makefiles"'
        MAKE = 'make -j%d' % (NUM_MAKE_PROCESSES,)

        if HAVE_DISTCC:
            CMAKE_PRE_VARS = 'CC="distcc cc" CXX="distcc c++"'
        else:
            CMAKE_PRE_VARS = ''

        SO_EXT = '.so'

    elif os.name == 'nt':
        CMAKE_DEFAULT_PARAMS = '-G "Visual Studio 8 2005"'
        # where the %s substitution is the SLN file
        # important that devenv is run, and NOT devenv.exe!
        MAKE = 'devenv %s /project %s ' \
            '/projectconfig "RelWithDebInfo|Win32" /build RelWithDebInfo'

        SO_EXT = '.dll'


