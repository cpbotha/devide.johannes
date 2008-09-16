# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import utils

dependencies = []

posix_script = """
#!/bin/bash

# johannes.py: setup environment ##################################

export PATH=%(python_binary_path)s:$PATH

unset LD_LIBRARY_PATH
unset PYTHONPATH

# python
LD_LIBRARY_PATH=%(python_library_path)s:$LD_LIBRARY_PATH
# wxpython
LD_LIBRARY_PATH=%(wx_lib_path)s:$LD_LIBRARY_PATH
PYTHONPATH=%(wxp_pythonpath)s:$PYTHONPATH
# VTK
LD_LIBRARY_PATH=%(vtk_sodir)s:$LD_LIBRARY_PATH
PYTHONPATH=%(vtk_python)s:%(vtk_sodir)s:$PYTHONPATH
# GDCM
LD_LIBRARY_PATH=%(gdcm_lib)s:$LD_LIBRARY_PATH
PYTHONPATH=%(gdcm_python)s:%(gdcm_lib)s:$PYTHONPATH
# vtkdevide
LD_LIBRARY_PATH=%(vtkdevide_lib)s:$LD_LIBRARY_PATH
PYTHONPATH=%(vtkdevide_python)s:%(vtkdevide_lib)s:$PYTHONPATH
# vtktudoss
LD_LIBRARY_PATH=%(vtktudoss_lib)s:$LD_LIBRARY_PATH
PYTHONPATH=%(vtktudoss_python)s:%(vtktudoss_lib)s:$PYTHONPATH
# ITK
LD_LIBRARY_PATH=%(itk_lib)s:%(wrapitk_lib)s:$LD_LIBRARY_PATH
PYTHONPATH=%(wrapitk_python)s:%(wrapitk_lib)s:$PYTHONPATH

# finally export
export LD_LIBRARY_PATH
export PYTHONPATH
"""

# we have to use %% where we want a single % due to the way python
# string interpolation works.  Python expects a single % to be
# followed by valid format specifiers.  Also see "Template strings"
# for a modern and simpler way to do string interpolation: 
# http://docs.python.org/lib/node40.html
nt_script = """
@rem johannes.py: setup environment ##################################

@rem zero the pythonpath for this session
@set PYTHONPATH=

@rem wxpython
@set PATH=%(wx_lib_path)s;%%PATH%%
@set PYTHONPATH=%(wxp_pythonpath)s;%%PYTHONPATH%%

@rem VTK
@set PATH=%(vtk_sodir)s;%%PATH%%
@set PYTHONPATH=%(vtk_python)s;%(vtk_sodir)s;%%PYTHONPATH%%

@rem GDCM
@set PATH=%(gdcm_lib)s;%%PATH%%
@set PYTHONPATH=%(gdcm_python)s;%(gdcm_lib)s;%%PYTHONPATH%%

@rem vtkdevide
@set PATH=%(vtkdevide_lib)s;%%PATH%%
@set PYTHONPATH=%(vtkdevide_python)s;%(vtkdevide_lib)s;%%PYTHONPATH%%

@rem vtktudoss
@set PATH=%(vtktudoss_lib)s;%%PATH%%
@set PYTHONPATH=%(vtktudoss_python)s;%(vtktudoss_lib)s;%%PYTHONPATH%%

@rem ITK
@set PATH=%(itk_bin)s;%(wrapitk_lib)s;%%PATH%%
@set PYTHONPATH=%(wrapitk_python)s;%(wrapitk_lib)s;%%PYTHONPATH%%
"""

class SetupEnvironment(InstallPackage):

    def install(self):

        vardict = {'python_binary_path' : config.python_binary_path,
                   'python_library_path' : config.python_library_path,
                   'wx_lib_path' : config.WX_LIB_PATH,
                   'wxp_pythonpath' : config.WXP_PYTHONPATH,
                   'vtk_sodir' : config.VTK_SODIR,
                   'vtk_python' : config.VTK_PYTHON,
                   'gdcm_lib' : config.GDCM_LIB,
                   'gdcm_python' : config.GDCM_PYTHON,
                   'vtkdevide_lib' : config.VTKDEVIDE_LIB,
                   'vtkdevide_python' : config.VTKDEVIDE_PYTHON,
                   'vtktudoss_lib' : config.VTKTUDOSS_LIB,
                   'vtktudoss_python' : config.VTKTUDOSS_PYTHON,
                   'itk_bin' : config.ITK_BIN,
                   'itk_lib' : config.ITK_DIR,
                   'wrapitk_lib' : config.WRAPITK_LIB,
                   'wrapitk_python' : config.WRAPITK_PYTHON}


        if os.name == 'nt':
            script = nt_script % vardict
            script_name = 'setup_env.cmd'
        else:
            script = posix_script % vardict
            script_name = 'setup_env.sh'

        script_fn = os.path.join(config.working_dir, script_name)
        sf = file(script_fn, 'w')
        sf.write(script)
        sf.close()

        utils.output('Wrote %s.' % (script_fn,))

    def get_installed_version(self):
        return None

