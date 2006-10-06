import config
from install_packages import wxpython, cmake, vtk, vtktud, vtkdevide, devide
import sys
import utils

def usage():
    print "johannes working_directory"

def main():
    if len(sys.argv) < 2:
        usage()

    else:
        config.init()

        rpad = 70
        rpad_char = '+'
        for ip in [wxpython.WXPython(), cmake.CMake(), vtk.VTK(),
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
