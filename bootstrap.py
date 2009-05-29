# python script for bootstrapping the johannes DeVIDE build system
#
# NB:
# 1. on unix systems that don't have Python installed, you should rather
# use bootstrap_stage1.sh and bootstrap_stage2.sh, these are
# shell-based alternatives to bootstrap.py
# 2. on windows systems, you have no choice: you need to have a system
# python installed to run this bootstrap.py script.
# 3. johannes.py will be run by the python that is locally built by
# EITHER bootstrap.py OR bootstrap_stage{1,2}.sh

import getopt
import sys

def usage():
    message = """
Invoke with:
    python bootstrap.py -w working_directory
    """

def main():
    try:
        optlist, args = getopt.getopt(
                sys.argv[1:], 'w',
                ['working-dir='])

    except getopt.GetoptError,e:
        usage()
        return

    working_dir = None

    for o, a in optlist:
        if o in ('-w', '--working-dir'):
            working_dir = a

    if not working_dir:
        usage()
        return
           

if __name__ == '__main__':
    main()

