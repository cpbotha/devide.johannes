import config
import getopt
from install_packages import numpy, matplotlib
from install_packages import wxpython, cmake, dcmtk
from install_packages import vtk
from install_packages import vtktud, vtkdevide
from install_packages import itk, itkvtkglue, itktud
from install_packages import installer, setupenvironment, devide
import sys
import utils

def usage():
    message = """
Welcome to johannes, the ugliest downloading/unpacking/configuring/building
and installation system of them all.  It could save you a lot of time though.
This instance of johannes will get, build and install the following: wxpython,
cmake, dcmtk, vtk, vtktud, vtkdevide, itk, itktud, itkvtkglue, devide

You need at least the following packages (or equivalents) on your system:
gcc, g++, bzip2-dev, ncurses-dev, gtk2-dev,
libfreetype-dev, libpng-dev, libzlib-dev (these three for matplotlib)

For a fast numeric python, you also need the libatlas-dev package.

Before starting johannes.py, first run bootstrap_stage1.sh and
bootstrap_stage2.sh to download and install python.  After that, run johannes
as follows:

/you/new/python johannes.py -w working_directory

Options are as follows:
-w, --working-dir      : specify working directory [REQUIRED]
-h, --help             : show this help
-m, --mode             : working mode, 'build' (default), 'clean_build' or
                         'get_only'
-p, --install-packages : specify comma-separated list of packages to work on,
                         default all

All of this ugliness is copyright 2006,2007 Charl P. Botha http://cpbotha.net/
and is hereby put under a BSD license.
"""

    print message

def main():
    if len(sys.argv) < 2:
        usage()

    else:
        rpad = 60
        rpad_char = '+'

        try:
            optlist, args = getopt.getopt(
                sys.argv[1:], 'hm:p:w:',
                ['help', 'mode=', 'install-packages=', 'working-dir='])

        except getopt.GetoptError,e:
            usage()
            return

        mode = 'build'
        install_packages = None
        working_dir = None
        profile = 'default'
        
        for o, a in optlist:
            if o in ('-h', '--help'):
                usage()
                return

            elif o in ('-m', '--mode'):
                if a in ('clean', 'clean_build'):
                    mode = 'clean_build'

            elif o in ('--install-packages'):
                # list of package name to perform the action on
                install_packages = [i.strip().lower() for i in a.split(',')]

            elif o in ('-w', '--working-dir'):
                working_dir = a

            elif o in ('--profile'):
                profile = a

        # we need at LEAST a working directory
        if not working_dir:
            usage()
            return

        # init config (DURR)
        config.init(working_dir, profile)

        ip_instance_list = [numpy.NumPy(),
                            wxpython.WXPython(),
                            matplotlib.matplotlib(),
                            cmake.CMake(),
                            dcmtk.DCMTK(),
                            vtk.VTK(),
                            vtktud.VTKTUD(),
                            vtkdevide.VTKDEVIDE(),
                            itk.ITK(),
                            itkvtkglue.ItkVtkGlue(),
                            itktud.ITKTUD(),
                            installer.Installer(),
                            setupenvironment.SetupEnvironment(),
                            devide.DeVIDE()]

        if install_packages is None:
            # iow the user didn't touch this
            # this only works because module and class names differ
            # ONLY w.r.t. case
            install_packages = [i.__class__.__name__.lower()
                                for i in ip_instance_list]

        def get_stage(ip, n):
            utils.output("%s :: get()" % (n,), rpad, rpad_char)
            ip.get()
        
        def unpack_to_install_stage(ip, n):
            utils.output("%s :: unpack()" % (n,), rpad, rpad_char)
            ip.unpack()
            utils.output("%s :: configure()" % (n,), rpad, rpad_char)
            ip.configure()
            utils.output("%s :: build()" % (n,), rpad, rpad_char)
            ip.build()
            utils.output("%s :: install()" % (n,), rpad, rpad_char)
            ip.install()
            
            
        
        for ip in ip_instance_list:
            n = ip.__class__.__name__.lower()
            if n in install_packages:

                if mode == 'get_only':
                    utils.output("%s GET_ONLY" % (n,), 70, '#')
                    utils.output("%s" % (n,), 70, '#')
                    get_stage(ip, n)

                if mode == 'build':
                    utils.output("%s" % (n,), 70, '#')
                    get_stage(ip, n)
                    unpack_to_install_stage(ip, n)

                elif mode == 'clean_build':
                    utils.output("%s CLEAN_BUILD" % (n,), 70, '#')
                    ip.clean_build()

if __name__ == '__main__':
    main()
