import config
import os
import sys, urllib
import tarfile

def output(message, rpad=0):
    s = "#####J> %s" % (message,)
    pn = rpad - len(s)
    if pn < 0:
        pn = 0
    p = pn * '#'
        
    print "%s %s" % (s,p)

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
    tar = tarfile.open(archive_filename, 'r|bz2')
    tar.extractall()
    tar.close()
