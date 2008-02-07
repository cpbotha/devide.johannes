# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
import getopt
from install_packages import numpy, matplotlib
from install_packages import wxpython, cmake, dcmtk
from install_packages import vtk
from install_packages import vtktudoss, vtkdevide
from install_packages import itk, itkvtkglue, itktudoss
from install_packages import installer, setupenvironment, devide
import os
import sys
import utils

def usage():
    message = """
Welcome to johannes, the ugliest
downloading/unpacking/configuring/building and installation system of
them all.  It could save you a lot of time though.  This instance of
johannes will get, build and install the following: python, numpy,
wxpython, matplotlib, cmake, dcmtk, vtk, vtktudoss, vtkdevide, itk,
itktudoss, itkvtkglue, devide

Please read the included README.txt file NOW.

Build method A (the default) is as follows: Before starting
johannes.py, first run bootstrap_stage1.sh and bootstrap_stage2.sh to
download and install python.  After that, run johannes as follows:

/you/new/python johannes.py -w working_directory

Options are as follows:
-w, --working-dir      : specify working directory [REQUIRED]
-h, --help             : show this help
-m, --mode             : working mode, 'everything' (default),
                         'clean_build', 'get_only' or 'configure_only'
-p, --install-packages : specify comma-separated list of packages to work on,
                         default all
--package-set          : preset collections of packages; vtkitk
--no-win-prereq        : do NOT do Windows prerequisites check.

All of this ugliness is copyright 2006-2008 Charl P. Botha http://cpbotha.net/
and is hereby put under a BSD license.
"""

    print message

def windows_prereq_check(working_dir):
    """Perform Windows system check for prerequisite software and
    directory structure.
    """

    utils.output("Windows prerequisites check", 70, '#')

    v = utils.find_command_with_ver(
            'MS Visual Studio', '%s /?' % (config.DEVENV,), 
            'Visual Studio Version (.*)\.$')

    v = v and utils.find_command_with_ver(
            'CMake', '%s --version' % (config.CMAKE_BINPATH,),
            '^cmake version\s+(.*)$')

    v = v and utils.find_command_with_ver(
            'CVS', '%s -v' % (config.CVS,),
            '\(CVS\)\s+(.*)\s+')

    v = v and utils.find_command_with_ver(
            'Subversion (SVN)', '%s --version' % (config.SVN,),
            'version\s+(.*)$')

    v = v and utils.find_command_with_ver(
            'patch', '%s -v' % (config.PATCH,),
            '^patch\s+(.*)$')

    # now check that working_dir contains the required subdirs
    dv = True
    for wsub in ['archive', 'build', 'inst']:
        cdir = os.path.join(working_dir, wsub)
        if os.path.isdir(cdir):
            msg = '%s exists.' % (cdir,)
        else:
            msg = '%s does not exist.' % (cdir,)
            dv = False

        utils.output(msg)

    return v and dv


def main():

    if len(sys.argv) < 2:
        usage()

    else:
        rpad = 60
        rpad_char = '+'

        try:
            optlist, args = getopt.getopt(
                sys.argv[1:], 'hm:p:w:',
                ['help', 'mode=', 'install-packages=', 
                    'package-set', 'working-dir=',
                    'no-win-prereq'])

        except getopt.GetoptError,e:
            usage()
            return

        mode = 'everything'
        install_packages = None
        working_dir = None
        profile = 'default'
        no_win_prereq = False
        
        for o, a in optlist:
            if o in ('-h', '--help'):
                usage()
                return

            elif o in ('-m', '--mode'):
                if a in ('clean', 'clean_build'):
                    mode = 'clean_build'
                elif a in ['get_only', 'unpack_only',
                        'configure_only']:
                    mode = a

            elif o in ('--install-packages'):
                # list of package name to perform the action on
                install_packages = [i.strip().lower() for i in a.split(',')]

            elif o in ('--package-set'):
                if a in ('vtkitk'):
                    install_packages = ['vtk', 'vtktudoss', 'vtkdevide',
                                        'itk', 'itkvtkglue',
                                        'itktudoss',
                                        'installer', 'setupenvironment',
                                        'devide']

            elif o in ('-w', '--working-dir'):
                working_dir = a

            elif o in ('--profile'):
                profile = a

            elif o in ('--no-win-prereq'):
                no_win_prereq = True

        # we need at LEAST a working directory
        if not working_dir:
            usage()
            return

        # init config (DURR)
        config.init(working_dir, profile)

        if os.name == 'nt' and not no_win_prereq:
            if not windows_prereq_check(working_dir):
                utils.output(
                     'Windows prerequisites do not check out.  '
                     'Fix and try again.', 70, '-')
                return
            else:
                utils.output(
                        'Windows prerequisites all good.', 70, '-')




        ip_instance_list = [numpy.NumPy(),
                            wxpython.WXPython(),
                            matplotlib.matplotlib(),
                            cmake.CMake(),
                            dcmtk.DCMTK(),
                            vtk.VTK(),
                            vtktudoss.VTKTUDOSS(),
                            vtkdevide.VTKDEVIDE(),
                            itk.ITK(),
                            itkvtkglue.ItkVtkGlue(),
                            itktudoss.ITKTUDOSS(),
                            installer.Installer(),
                            setupenvironment.SetupEnvironment(),
                            devide.DeVIDE()]

        if install_packages is None:
            # iow the user didn't touch this
            # this only works because module and class names differ
            # ONLY w.r.t. case
            install_packages = [i.__class__.__name__.lower()
                                for i in ip_instance_list]

        # if we're on windows, remove a number of packages regardless
        # of user preferences.  Sorry user!
        if os.name == 'nt':
            nogo = ['numpy', 'wxpython', 'matplotlib', 'cmake']
            install_packages = [i for i in install_packages if i not
                    in nogo]

        def get_stage(ip, n):
            utils.output("%s :: get()" % (n,), rpad, rpad_char)
            ip.get()

        def unpack_stage(ip, n):
            utils.output("%s :: unpack()" % (n,), rpad, rpad_char)
            ip.unpack()

        def configure_stage(ip, n):
            utils.output("%s :: configure()" % (n,), rpad, rpad_char)
            ip.configure()

        def build_stage(ip, n):
            utils.output("%s :: build()" % (n,), rpad, rpad_char)
            ip.build()

        def all_stages(ip, n):
            get_stage(ip, n)

            unpack_stage(ip, n)

            configure_stage(ip, n)            

            build_stage(ip, n)
            
            utils.output("%s :: install()" % (n,), rpad, rpad_char)
            ip.install()
            
        
        for ip in ip_instance_list:
            n = ip.__class__.__name__.lower()
            if n in install_packages:

                if mode == 'get_only':
                    utils.output("%s GET_ONLY" % (n,), 70, '#')
                    utils.output("%s" % (n,), 70, '#')
                    get_stage(ip, n)

                elif mode == 'unpack_only':
                    utils.output("%s UNPACK_ONLY" % (n,), 70, '#')
                    utils.output("%s" % (n,), 70, '#')
                    unpack_stage(ip, n)

                elif mode == 'configure_only':
                    utils.output("%s CONFIGURE_ONLY" % (n,), 70, '#')
                    utils.output("%s" % (n,), 70, '#')
                    configure_stage(ip, n)

                elif mode == 'everything':
                    utils.output("%s" % (n,), 70, '#')
                    all_stages(ip, n)

                elif mode == 'clean_build':
                    utils.output("%s CLEAN_BUILD" % (n,), 70, '#')
                    ip.clean_build()

if __name__ == '__main__':
    main()
