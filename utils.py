import config
import os
import re
import sys, urllib
import shutil
import tarfile

def output(message, rpad=0, rpad_char='#'):
    s = "#####J> %s" % (message,)
    pn = rpad - len(s)
    if pn < 0:
        pn = 0
    p = pn * rpad_char
        
    print "%s %s" % (s,p)

def error(message):
    raise RuntimeError('!!!!! %s' % (message,))

def urlget(url):
    """Simple method to retrieve URL.  It will get the file in the current
    directory.
    """
    
    def reporthook(blocknum, blocksize, totalsize):
        current_size = blocknum * blocksize
        current_size_kb = int(current_size / 1024.0)
        sys.stdout.write(
            '% 4.0f %% (%d Kbytes) downloaded\r' %
            (current_size / float(totalsize) * 100.0, current_size_kb))

    i = url.rfind('/')
    filename = url[i+1:]
    print url, "->", filename
    if os.path.exists(filename):
        output("%s already present, skipping download." % (filename,))

    else:
        urllib.urlretrieve(url, filename, reporthook)
        sys.stdout.write("\n")
        output("Download complete.")

    return filename


def goto_archive():
    os.chdir(config.archive_dir)

def goto_build():
    os.chdir(config.build_dir)

def unpack_build(archive_filename):
    """Unpack given archive_filename in build directory.
    """
    goto_build()

    if archive_filename.lower().endswith('bz2'):
        m = 'r|bz2'
    else:
        m = 'r|gz'
        
    tar = tarfile.open(archive_filename, m)
    tar.extractall()
    tar.close()

def re_sub_filter_file(repls, filename):
    """Given a list of repls (tuples with regular expresions and
    replacement patterns that are used as the first and second params
    of re.sub), filter filename line by line.

    A backup of the file is made to filename.orig.
    """

    newfilename = '%s.new' % (filename,)
    origfilename = '%s.orig' % (filename,)

    shutil.copyfile(filename, origfilename)

    ifile = file(filename)
    ofile = file(newfilename, 'w')

    for l in ifile:
        for r in repls:
            l = re.sub(r[0], r[1], l)

        ofile.write(l)

    ifile.close()
    ofile.close()
            
    shutil.copyfile(newfilename, filename)
