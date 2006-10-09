#!/bin/bash
# script for bootstrapping johannes DeVIDE build system
# copyright cpbotha.net

if [ -z $1 ]; then
echo "Specify working directory as first parameter."
exit;
fi

p=$1/inst/python/bin/python
if [ -f $p ]; then
echo "It seems that bootstrap.sh has already executed."
echo "If you want to run it again, delete $p."
exit
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
./configure --enable-shared --prefix=$WD/inst/python

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

cd $WD
echo "#!/bin/sh" > setup_env.sh
echo "export LD_LIBRARY_PATH=$WD/inst/python/lib"
echo "export PATH=$WD/inst/python/bin/:$PATH"

echo "JOHANNES #####"
echo "Successfully built Python.  Start the build system with "
echo ". $WD/setup_env.sh"
echo "$WD/inst/python/bin/python johannes.py -w $WD"
