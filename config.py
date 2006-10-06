# FIXME: we could do more in this module to abstract OS differences
# for example, we could have a build command that varies per platform
# WIN32: 'devenv %s /project ALL_BUILD /projectconfig \
# "RelWithDebInfo|Win32" /build RelWithDebInfo'
# IX: make

import os
import sys

# for binaries not on your PATH, you should specify the complete path here
# otherwise only the binary name
SVN = '/usr/bin/svn'
CVS = '/usr/bin/cvs'
PATCH = 'patch'
# this should move to the platform dependent part of init()
MAKE = 'make -j2' # if you have more CPUS, up the -j parameter!


# nothing for you to edit below this line
#######################################################################

CMAKE = '' # this will be set by the cmake InstallPackage when it runs
CMAKE_DEFAULT_PARAMS = '' # this will be set by init()

VTK_DIR = '' # this will be set by the vtk InstallPackage
VTK_LIB = ''
VTK_PYTHON = ''

WX_LIB_PATH = '' # will be set by wxpython InstallPackage
WXP_PYTHONPATH = '' # will be set by wxpython InstallPackage

DEVIDE_PY = '' # written by devide InstallPackage

def init():
    global working_dir, archive_dir, build_dir, inst_dir
    working_dir = os.path.abspath(sys.argv[1])
    archive_dir = os.path.join(working_dir, 'archive')
    build_dir = os.path.join(working_dir, 'build')
    inst_dir = os.path.join(working_dir, 'inst')

    global python_include_path, python_library, python_binary_path
    python_include_path = os.path.join(inst_dir, 'python/include/python2.5')
    python_library = os.path.join(
        inst_dir, 'python/lib/python2.5/config/libpython2.5.a')
    python_binary_path = os.path.join(inst_dir, 'python/bin')

    # platform dependent stuff =========================================
    # use conditionals based on os.name (posix, nt) and sys.platform (linux2,
    # win32)

    global CMAKE_DEFAULT_PARAMS

    if os.name == 'posix':
        CMAKE_DEFAULT_PARAMS = '-G "Unix Makefiles"'

    elif os.name == 'nt':
        CMAKE_DEFAULT_PARAMS = '-G "Visual Studio 7 .NET 2003"'
