import os
import sys

WXP_URL = "http://surfnet.dl.sourceforge.net/sourceforge/wxpython/wxPython-src-2.6.3.3.tar.bz2"

def init():
    global working_dir, archive_dir, build_dir, inst_dir
    working_dir = os.path.abspath(sys.argv[1])
    archive_dir = os.path.join(working_dir, 'archive')
    build_dir = os.path.join(working_dir, 'build')
    inst_dir = os.path.join(working_dir, 'inst')
