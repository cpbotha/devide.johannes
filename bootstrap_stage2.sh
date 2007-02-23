#!/bin/bash
# script for bootstrapping johannes DeVIDE build system
# copyright cpbotha.net

if [ -z $1 ]; then
echo "Specify working directory as first parameter."
exit;
fi

FLAG_FILE1=$1/flags/stage1_complete
FLAG_FILE2=$1/flags/stage2_complete

p=$1/inst/python/bin/python
if [ -f $p ]; then
echo "It seems that bootstrap_stage2.sh has already executed."
echo "If you want to run it again, delete $p."
exit
fi

if [ ! -f $FLAG_FILE1 ]; then
echo "You have to run bootstrap_stage1.sh before you run stage2."
exit
fi

cd $1
WD=`pwd`

cd build
tar xjvf ../archive/Python-2.4.4.tar.bz2
cd Python-2.4.4
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

ENV_FILE=python_setup_env.sh
echo "#!/bin/sh" > $ENV_FILE
echo "export LD_LIBRARY_PATH=$WD/inst/python/lib" >> $ENV_FILE
echo "export PATH=$WD/inst/python/bin/:\$PATH" >> $ENV_FILE

echo "JOHANNES #####"
echo "Successfully built Python.  Start the build system with "
echo ". $WD/$ENV_FILE"
echo "$WD/inst/python/bin/python johannes.py -w $WD"

cd flags
touch $FLAG_FILE2
cd $WD
