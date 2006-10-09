import config
from install_package import InstallPackage
import os
import utils

class SetupEnvironment(InstallPackage):

    def install(self):

        vardict = {'python_binary_path' : config.python_binary_path,
                   'python_library_path' : config.python_library_path,
                   'wx_lib_path' : config.WX_LIB_PATH,
                   'wxp_pythonpath' : config.WXP_PYTHONPATH,
                   'vtk_lib' : config.VTK_LIB,
                   'vtk_python' : config.VTK_PYTHON,
                   'vtkdevide_lib' : config.VTKDEVIDE_LIB,
                   'vtkdevide_python' : config.VTKDEVIDE_PYTHON,
                   'vtktud_lib' : config.VTKTUD_LIB,
                   'vtktud_python' : config.VTKTUD_PYTHON,
                   'itk_lib' : config.ITK_DIR,
                   'wrapitk_lib' : config.WRAPITK_LIB,
                   'wrapitk_python' : config.WRAPITK_PYTHON}


        script = """
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
LD_LIBRARY_PATH=%(vtk_lib)s:$LD_LIBRARY_PATH
PYTHONPATH=%(vtk_python)s:%(vtk_lib)s:$PYTHONPATH
# vtkdevide
LD_LIBRARY_PATH=%(vtkdevide_lib)s:$LD_LIBRARY_PATH
PYTHONPATH=%(vtkdevide_python)s:%(vtkdevide_lib)s:$PYTHONPATH
# vtktud
LD_LIBRARY_PATH=%(vtktud_lib)s:$LD_LIBRARY_PATH
PYTHONPATH=%(vtktud_python)s:%(vtktud_lib)s:$PYTHONPATH
# ITK
LD_LIBRARY_PATH=%(itk_lib)s:%(wrapitk_lib)s:$LD_LIBRARY_PATH
PYTHONPATH=%(wrapitk_python)s:%(wrapitk_lib)s:$PYTHONPATH

# finally export
export LD_LIBRARY_PATH
export PYTHONPATH
        """ % vardict

        script_fn = os.path.join(config.working_dir, 'setup_env.sh')
        sf = file(script_fn, 'w')
        sf.write(script)
        sf.close()

        utils.output('Wrote %s.' % (script_fn,))
