import config
from install_packages import wxpython, cmake, dcmtk
from install_packages import vtk, vtktud, vtkdevide, devide
import sys
import utils

def usage():
    message = """
Welcome to johannes, the ugliest downloading/unpacking/configuring/building
and installation system of them all.  It could save you a lot of time though.
This instance of johannes will get, build and install the following: wxpython,
cmake, dcmtk, vtk, vtktud, vtkdevide, devide

Before starting johannes.py, first run bootstrap.sh to download and install
python.  After that, run johannes as follows:

/you/new/python johannes.py working_directory

All of this ugliness is copyright 2006 Charl P. Botha http://cpbotha.net/
and is hereby put under a BSD license.
"""

    print message

def main():
    if len(sys.argv) < 2:
        usage()

    else:
        config.init()

        rpad = 70
        rpad_char = '+'
        for ip in [wxpython.WXPython(), cmake.CMake(), dcmtk.DCMTK(),
                   vtk.VTK(),
                   vtktud.VTKTUD(), vtkdevide.VTKDEVIDE(), devide.DeVIDE()]:
            n = ip.__module__
            utils.output("%s" % (n,), rpad, '#')
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

if __name__ == '__main__':
    main()
