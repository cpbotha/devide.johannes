#!/bin/bash
# script for bootstrapping johannes DeVIDE build system
# copyright cpbotha.net

if [ -z $1 ]; then
echo "Specify working directory as first parameter."
exit;
fi

mkdir $1
cd $1

WD=`pwd`

mkdir archive
mkdir build
mkdir inst

cd archive
wget -c http://www.python.org/ftp/python/2.5/Python-2.5.tar.bz2
cd ../build
tar xjvf ../archive/Python-2.5.tar.bz2
cd Python-2.5
./configure --prefix=$WD/inst/python

if [ "$?" -ne "0" ]; then
echo "JOHANNES ##### Python config error.  Please fix errors and try again."
exit
fi

make
make install

if [ "$?" -ne "0" ]; then
echo "JOHANNES ##### Python build error.  Please fix errors and try again."
exit
fi

echo "JOHANNES #####"
echo "Successfully built Python.  Start the build system with "
echo "$WD/inst/python/bin/python johannes.py $WD"
