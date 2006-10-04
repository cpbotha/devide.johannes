import config
from install_packages import wxpython
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
        for ip in [wxpython.WXPython()]:
            n = ip.__module__
            utils.output("%s :: get()" % (n,), rpad)
            ip.get()
            utils.output("%s :: unpack()" % (n,), rpad)
            ip.unpack()
            utils.output("%s :: configure()" % (n,), rpad)
            ip.configure()
            utils.output("%s :: build()" % (n,), rpad)
            ip.build()
            utils.output("%s :: install()" % (n,), rpad)
            ip.install()

if __name__ == '__main__':
    main()
