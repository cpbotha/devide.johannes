import config
import os
import sys, urllib
import tarfile

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
        print "%s already present, skipping download." % (filename,)

    else:
        urllib.urlretrieve(url, filename, reporthook)
        print "Download complete."

    return filename


def goto_archive():
    os.chdir(config.archive_dir)

def goto_build():
    os.chdir(config.build_dir)

def urlget_and_unpack(url):
    print "##### Downloading."
    goto_archive()
    filename = urlget(url)
    full_filename = os.path.join(config.archive_dir, filename)

    print "##### Unpacking %s" % (filename,)
    goto_build()
    tar = tarfile.open(full_filename, 'r|bz2')
    tar.extractall()
    tar.close()
