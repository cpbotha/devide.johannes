#!/bin/bash
# stage1 script for bootstrapping johannes DeVIDE build system
# this will create the working directory tree and download the python tarball
# copyright cpbotha.net

if [ -z $1 ]; then
echo "Specify working directory as first parameter."
exit;
fi

FLAG_FILE=$1/flags/stage1_complete

if [ -f $FLAG_FILE ]; then
echo "It seems that bootstrap_stage1.sh has already executed."
echo "If you want to force re-execution, remove $FLAG_FILE"
echo "then try again."
exit
fi

mkdir $1
cd $1

WD=`pwd`

# * tarballs get downloaded in archive
# * checkouts also get done in archive for things that support out of
#   source builds
# johannes should be able to do its whole thing without an internet connection
# if archive has been properly filled.
mkdir archive
mkdir build
mkdir flags
mkdir inst

cd archive
wget -c http://python.org/ftp/python/2.5.4/Python-2.5.4.tar.bz2

cd ../flags
touch stage1_complete


cd $WD

