import config
import getopt
from install_packages import wxpython, cmake, dcmtk
from install_packages import vtk
from install_packages import itk
from install_packages import vtktud, vtkdevide, devide
import sys
import utils

def usage():
    message = """
Welcome to johannes, the ugliest downloading/unpacking/configuring/building
and installation system of them all.  It could save you a lot of time though.
This instance of johannes will get, build and install the following: wxpython,
cmake, dcmtk, vtk, vtktud, vtkdevide, devide

You need at least the following packages (or equivalents) on your system:
gcc, g++, bzip2-dev, ncurses-dev, gtk2-dev

Before starting johannes.py, first run bootstrap.sh to download and install
python.  After that, run johannes as follows:

/you/new/python johannes.py -w working_directory

Options are as follows:
-w, --working-dir      : specify working directory [REQUIRED]
-h, --help             : show this help
-m, --mode             : working mode, 'build' (default) or 'clean_build'
-p, --install-packages : specify comma-separated list of packages to work on,
                         default all

All of this ugliness is copyright 2006 Charl P. Botha http://cpbotha.net/
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

        # we need at LEAST a working directory
        if not working_dir:
            usage()
            return

        # init config (DURR)
        config.init(working_dir)


        ip_instance_list = [wxpython.WXPython(),
                            cmake.CMake(),
                            dcmtk.DCMTK(),
                            vtk.VTK(),
                            itk.ITK(),
                            vtktud.VTKTUD(),
                            vtkdevide.VTKDEVIDE(),
                            devide.DeVIDE()]

        if install_packages is None:
            # iow the user didn't touch this
            # this only works because module and class names differ
            # ONLY w.r.t. case
            install_packages = [i.__class__.__name__.lower()
                                for i in ip_instance_list]
        
        for ip in ip_instance_list:
            n = ip.__class__.__name__.lower()
            if n in install_packages:

                if mode == 'build':
                    utils.output("%s" % (n,), 70, '#')
                    utils.output("%s :: get()" % (n,), rpad, rpad_char)
                    ip.get()
                    utils.output("%s :: unpack()" % (n,), rpad, rpad_char)
                    ip.unpack()
                    utils.output("%s :: configure()" % (n,), rpad, rpad_char)
                    ip.configure()
                    utils.output("%s :: build()" % (n,), rpad, rpad_char)
                    ip.build()
                    utils.output("%s :: install()" % (n,), rpad, rpad_char)
                    ip.install()

                elif mode == 'clean_build':
                    utils.output("%s CLEAN_BUILD" % (n,), 70, '#')
                    ip.clean_build()

if __name__ == '__main__':
    main()
