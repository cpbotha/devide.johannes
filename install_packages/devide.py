import config
from install_package import InstallPackage
import os
import utils

BASENAME = "devide"
SVN_REPO = "https://stockholm.twi.tudelft.nl/svn/devide/trunk/" + BASENAME

class DeVIDE(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.build_dir, BASENAME)

    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("DeVIDE already checked out, skipping step.")

        else:
            os.chdir(config.build_dir)
            ret = os.system("%s co %s" % (config.SVN, SVN_REPO))
            if ret != 0:
                utils.error("Could not SVN checkout DeVIDE.  "
                            "Fix and try again.")

    def install(self):
        # setup some devide config variables
        config.DEVIDE_PY = os.path.join(self.source_dir, 'devide.py')
        
        # write script for starting up devide
        vardict = {'python_binary_path' : config.python_binary_path,
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
                   'wrapitk_python' : config.WRAPITK_PYTHON,
                   'devide_py' : config.DEVIDE_PY}

        script = """
#!/bin/bash
        
# setup environment #######################################
export PATH=%(python_binary_path)s:$PATH
unset LD_LIBRARY_PATH
unset PYTHONPATH
# wxpython
LD_LIBRARY_PATH=%(wx_lib_path)s
PYTHONPATH=%(wxp_pythonpath)s
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

# invoke DeVIDE ###########################################
python %(devide_py)s --no-kits itk_kit,numpy_kit,matplotlib_kit $*
        """ % vardict

        invoking_script_fn = os.path.join(config.working_dir, 'devide.sh')
        isf = file(invoking_script_fn, 'w')
        isf.write(script)
        isf.close()

        utils.output('Wrote %s.  Use this to startup DeVIDE!' %
                     (invoking_script_fn,))

               
