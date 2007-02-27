# FIXME: we could do more in this module to abstract OS differences
# for example, we could have a build command that varies per platform
# WIN32: 'devenv %s /project ALL_BUILD /projectconfig \
# "RelWithDebInfo|Win32" /build RelWithDebInfo'
# IX: make

# FIXME: each installpackage should be able to register its own
# library and python paths.  At the moment, devide.py is taking care
# of creating the script containing all these... (not optimal!)

import os
import sys

# for binaries not on your PATH, you should specify the complete path here,
# e.g. SVN = '/usr/bin/svn'.  For binaries ON your path, only the binary name
# e.g. SVN = 'svn'
SVN = 'svn'
CVS = 'cvs -z3'
PATCH = 'patch'
# this should move to the platform dependent part of init()
MAKE = 'make -j2' # if you have more CPUS, up the -j parameter!


# nothing for you to edit below this line
#######################################################################

# the following variables are written by various InstallPackages
CMAKE = '' 
CMAKE_DEFAULT_PARAMS = '' # this will be set by init()

DCMTK_INCLUDE = ''
DCMTK_LIB = ''

VTK_DIR = ''
VTK_LIB = ''
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

    global python_include_path, python_library_path, python_library, \
           python_binary_path
    python_include_path = os.path.join(inst_dir, 'python/include/python2.4')
    python_library_path = os.path.join(inst_dir, 'python/lib')
    python_library = os.path.join(python_library_path, 'libpython2.4.so')
    python_binary_path = os.path.join(inst_dir, 'python/bin')

    # platform dependent stuff =========================================
    # use conditionals based on os.name (posix, nt) and sys.platform (linux2,
    # win32)

    global CMAKE_DEFAULT_PARAMS

    if os.name == 'posix':
        CMAKE_DEFAULT_PARAMS = '-G "Unix Makefiles"'

    elif os.name == 'nt':
        CMAKE_DEFAULT_PARAMS = '-G "Visual Studio 7 .NET 2003"'
