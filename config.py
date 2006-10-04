import os
import sys

SVN = '/usr/bin/svn'
CVS = '/usr/bin/cvs'

def init():
    global working_dir, archive_dir, build_dir, inst_dir
    working_dir = os.path.abspath(sys.argv[1])
    archive_dir = os.path.join(working_dir, 'archive')
    build_dir = os.path.join(working_dir, 'build')
    inst_dir = os.path.join(working_dir, 'inst')
