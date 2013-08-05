This package contains Clinical Graphics' clone of johannes, a very scary build 
system that was originally designed to build DeVIDE under *ix.

JohannesCG is intended for building Articulis' dependencies under Windows(tm) 
in all bits (especially 64). See LINUX.txt for doing the same under *ix.

The original johannes is copyright 2007-2011 Charl P. Botha <cpbotha@vxlabs.com>
and is made available under the New BSD License.
Original at http://code.google.com/p/devide/source/browse/README.txt?repo=johannes

Without further ado, this is how you get johannesCG working on your Windows:

0. Before you start:
--------------------
Due to certain issues on Windows (primarily the difficulty of building
Python extensions automatically if you don't have the exact same
compiler as Python), johannesCG can NOT build the basic stuff on
Windows.

However, it IS able to build the more complex stuff, such as dcmtk,
itk, vtk and other high-level dependencies of DeVIDE and Articulis.


1. First get and install all the prerequisites:
-----------------------------------------------

* Get and install Python 2.6 from [1].  This will only be used for
  bootstrapping, so a Python 2.5 should also do.
* SVN: get and install the command-line client from [2].
  The installer will modify your PATH variable. 
* GIT: get and install the Windows installer (Git-1.7.4-*.exe at the time
  of this writing) from http://git-scm.com/
  Select the option where you can run git from a cmd window (second of the three)
  NOTE: GIT should use the platform's default line endings when checking out a repo.
        On Windows this is "CRLF", as required for Gnu32 patch.exe.
        (you can check that "git config --global core.autocrlf" is set to "true" instead of "input")
* mercurial: get and install Windows installer (Mercurial-2.1-x*.exe at 
  the time of this writing) from http://mercurial.selenic.com/downloads/
  Let the installer add the installation path to the system search path.
  Also: You'll have better luck with the win32 installer - even on win64.
  NOTE: You must have Mercurial's EOL extention enabled otherwise you will have problems with gnu32 patch.
  Instructions at: http://mercurial.selenic.com/wiki/EolExtension
  (NB: Windows Explorer doesn't allow the creation of a file called .hgrc due to the preceding "." - you either have to use the command line to name it, use its alternative name: mercurial.ini)
* CVS: get the WinCVS ZIP from 
  http://sourceforge.net/projects/cvsgui/files/WinCvs/WinCvs%202.0.2-4/WinCvs2_0_2-4.zip/download
  and then extract the CVSNT installer
  from there and install it.  The installer will modify your PATH
  variable.
* patch: get from http://gnuwin32.sourceforge.net/packages/patch.htm
  and install.  Add its install directory to your path.
  NB: On Windows 7, the gnuwin32 patch will segfault. Follow the instructions
  on http://math.nist.gov/oommf/software-patchsets/patch_on_Windows7.html
  to fix. In short this is what the fix entails:
  In johannes' /patches subdirectory you will find a file called "patch.exe.manifest".
  Copy this file to the same directory as Gnu32's "patch.exe".
  Then, run a Visual Studio command prompt as administrator, and execute the following command:
    mt -manifest patch.exe.manifest -outputresource:patch.exe;1  
  This installs the manifest *into* the patch.exe binary (but it could possibly already be sufficient just to store the patch.exe.manifest in the same folder as patch.exe). 
  Lastly, move patch.exe out from under C:\Program Files (x86) to a path that contains no spaces, 
  and make sure that it is in the system path. (not sure if spaces create a problem, but let's not take chances)
* Get and install the NSIS installer builder from [3].  Put its install
  directory on your system PATH.
* Visual Studio 2008: Make sure the latest service pack installed, SP1
  at the time of this writing (August 1, 2009).  Add the Visual Studio
  2008 devenv.com directory to your path.  On this win32 image,
  that's: C:\Program Files\Microsoft Visual Studio 9.0\Common7\IDE

I can recommend cpbotha.net/software/envedit for easy path editing.
It's BSD open source by yours truly.

[1] http://www.python.org/ftp/python/2.6.2/python-2.6.2.msi
[2] http://www.sliksvn.com/pub/Slik-Subversion-1.6.17-win32.msi
[3] http://sourceforge.net/projects/nsis/files/NSIS%202/2.45/nsis-2.45-setup.exe/download

2. Now let johannes do its magic:
---------------------------------

The packages that johannesCG will build are specified in the johannes.cfg file in the working directory.

Here is the line in johannes.cfg that specifies the packages you would typically want to build for Articulis:
packages = CMake, VTK56CG, ITK, VTKDEVIDE, SWIG, CableSwig, WrapITK, ItkVtkGlue, VTKTUDCG, GDCM

python \where\you\put\it\bootstrap.py -w your_working_dir
your_working_dir\jpython \where\you\put\it\johannes.py -w your_working_dir

Wait a few hours. 
In principle all built binaries should be written to separate directories in in \inst subdirectory, however since some
packages' scripts have not been sufficiently refined you may have to scour the \build directory for the required built 
binaries (and especially the python wrappers), where they will be available along with all the temporary build files (making it quite a large amount of data to copy around).
The best advice is to follow Articulis' build-environment-setup documentation, where these things are spelt out.

APPENDIX:
---------

If you want to command johannes from the command line to e.g. just VTK and/or ITK.  You can!

Follow all instructions under 1., then do for example:

your_working_dir\jpython \where\you\put\it\johannes.py -w your_working_dir -p itk,vtk

See johannes --help for clues to package names