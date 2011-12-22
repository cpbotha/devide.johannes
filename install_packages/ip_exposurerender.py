# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import re
import shutil
import sys
import utils

BASENAME = "ExposureRender"
GIT_REPO = "http://code.google.com/p/exposure-render"
#GIT_TAG = "v5.6.1"

dependencies = ['CMake', 'Qt', 'VTK_QT_58']
                  
class ExposureRender(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.archive_dir, BASENAME)
        self.build_dir = os.path.join(config.build_dir, '%s' %
                                      (BASENAME,))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)
    
    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("Exposure Render already checked out, skipping step.")

        else:
            utils.goto_archive()
            
            ret = os.system("hg clone %s %s" % (GIT_REPO, BASENAME))
            if ret != 0:
                utils.error("Could not clone Exposure Render repository.  Fix and try again.")
            
            os.chdir(self.source_dir)
            ret = os.system("hg update") #TODO: is this required?
            if ret != 0:
                utils.error("Could not update Exposure Render. Fix and try again.")

    def configure(self):
        if os.path.exists(
           os.path.join(self.build_dir, 'CMakeFiles/cmake.check_cache')):
           utils.output("Exposure Render build already configured.")
           return
        
        if not os.path.exists(self.build_dir):
            os.mkdir(self.build_dir)
        
        QT_MOC_EXECUTABLE = os.path.join(config.QT_BIN, 'moc.exe')
        QT_QMAKE_EXECUTABLE = os.path.join(config.QT_BIN, 'qmake.exe')
        QT_UIC_EXECUTABLE = os.path.join(config.QT_BIN, 'uic.exe')
       
        
		#if not os.path.exists(QT_MOC_EXECUTABLE):
        #    print "Qt MOC executable not found, aborting!"
         #    return;


		
        cmake_params = \
                "-DBUILD_SHARED_LIBS=ON " \
                "-DCMAKE_BUILD_TYPE=RelWithDebInfo " \
                "-DCMAKE_INSTALL_PREFIX=%s " \
                "-DPYTHON_INCLUDE_DIR=%s " \
                "-DPYTHON_LIBRARY=%s " \
                "-DQT_MOC_EXECUTABLE=%s " \
                "-DQT_QMAKE_EXECUTABLE=%s " \
                "-DQT_UIC_EXECUTABLE=%s " \
                "-DVTK_DIR:PATH=%s" \
                                % (self.inst_dir,
                                   config.PYTHON_INCLUDE_PATH,
                                   config.PYTHON_LIBRARY,
                                   QT_MOC_EXECUTABLE,
                                   QT_QMAKE_EXECUTABLE,
                                   QT_UIC_EXECUTABLE,
								   config.VTK_DIR)
								   
        ret = utils.cmake_command(self.build_dir, os.path.join(self.source_dir, 'Source'), cmake_params)
        
        if ret != 0:
            utils.error("Could not configure Exposure Render.  Fix and try again.")
		
    def build(self):
        posix_file = os.path.join(self.build_dir, config.BUILD_TARGET,
            'libvtkErCorePython.so') #TODO: check whether this is the correct file to test on
        nt_file = os.path.join(self.build_dir, config.BUILD_TARGET, 
                'vtkErCorePythonD.dll')
        
        if utils.file_exists(posix_file, nt_file):
            utils.output("Exposure Render already built.  Skipping build step.")

        else:
            os.chdir(self.build_dir)
            ret = utils.make_command('ErGUI.sln')
            if ret != 0:
                utils.error("Error building Exposure Render.  Fix and try again.")

    def install(self):
        posix_file = os.path.join(self.inst_dir, 'bin/ErGUI')
        nt_file = os.path.join(self.inst_dir, 'bin', 'ErGUI.exe')

        if utils.file_exists(posix_file, nt_file):    
            utils.output("Exposure Render already installed.  Skipping install step.")

        else:
			ret = utils.make_command('ErGUI.sln', install=True)
			if ret != 0:
				utils.error("Could not install Exposure Render.  Fix and try again.")

        
    def clean_build(self):
        utils.output("Removing build and installation directories.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

        self.clean_install()
        
    def clean_install(self):
        utils.output("Removing installation directory.")
        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)
    
    def get_installed_version(self):
		#TODO: implement
		return ''
        
