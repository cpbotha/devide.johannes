# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

from ip_vtk58 import VTK58
import os
import utils
import config

dependencies = ['CMake', 'Qt']

class VTK_QT_58(VTK58):
    
    def configure(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'CMakeFiles/cmake.check_cache')):
            utils.output("VTK build already configured.")
            return
        
        if not os.path.exists(self.build_dir):
            os.mkdir(self.build_dir)

        QT_MOC_EXECUTABLE = os.path.join(config.QT_BIN, 'moc.exe')
        QT_QMAKE_EXECUTABLE = os.path.join(config.QT_BIN, 'qmake.exe')
        QT_UIC_EXECUTABLE = os.path.join(config.QT_BIN, 'uic.exe')
        cmake_params = "-DBUILD_SHARED_LIBS=ON " \
                       "-DBUILD_TESTING=OFF " \
                       "-DCMAKE_BUILD_TYPE=RelWithDebInfo " \
                       "-DCMAKE_INSTALL_PREFIX=%s " \
		               "-DVTK_USE_TK=NO " \
                       "-DVTK_USE_METAIO=ON " \
                       "-DVTK_USE_PARALLEL=ON " \
                       "-DPYTHON_EXECUTABLE=%s " \
                       "-DPYTHON_LIBRARY=%s " \
                       "-DPYTHON_INCLUDE_PATH=%s " \
                       "-DVTK_USE_GUISUPPORT=ON " \
                       "-DVTK_USE_QT=ON " \
                       "-DVTK_USE_QVTK_QTOPENGL=ON " \
                       "-DVTK_WRAP_PYTHON=ON " \
                       "-DQT_MOC_EXECUTABLE=%s " \
                       "-DQT_QMAKE_EXECUTABLE=%s " \
                       "-DQT_UIC_EXECUTABLE=%s " \
                                              % (self.inst_dir,
                                                 config.PYTHON_EXECUTABLE,
                                                 config.PYTHON_LIBRARY,
                                                 config.PYTHON_INCLUDE_PATH,
                                                 QT_MOC_EXECUTABLE,
                                                 QT_QMAKE_EXECUTABLE,
                                                 QT_UIC_EXECUTABLE)
        
        ret = utils.cmake_command(self.build_dir, self.source_dir,
                cmake_params)

        if ret != 0:
            utils.error("Could not configure VTK.  Fix and try again.")
                       
