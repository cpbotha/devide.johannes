# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import utils

dependencies = []

posix_cfg = """
[env:ld_library_path]
python: %(python_library_paths)s
wxpython: %(wx_lib_path)s

"""

nt_cfg = """
# DRE config written by johannes build system
# %%(dre_top)s will be replaced by the DRE top-level directory.

[env:path]
wxpython: %(wx_lib_path)s
vtk: %(vtk_sodir)s
gdcm: %(gdcm_lib)s
vtkdevide: %(vtkdevide_lib)s
vtktudoss: %(vtktudoss_lib)s
itk:%(itk_bin)s;%(wrapitk_lib)s

[env:pythonpath]
vtk: %(vtk_python)s;%(vtk_sodir)s
gdcm: %(gdcm_python)s;%(gdcm_lib)s
vtkdevide: %(vtkdevide_python)s;%(vtkdevide_lib)s
vtktudoss:%(vtktudoss_python)s;%(vtktudoss_lib)s
itk:%(wrapitk_python)s;%(wrapitk_lib)s

"""

posix_scripts = {'inc': ('paths.inc', """
# include file used by other DeVIDE scripts
# make sure invoking script has set MYDIR

PATH=%(python_binary_path)s:$PATH

unset LD_LIBRARY_PATH
unset PYTHONPATH

# python
LD_LIBRARY_PATH=%(python_library_path)s:$LD_LIBRARY_PATH
# wxpython
LD_LIBRARY_PATH=%(wx_lib_path)s:$LD_LIBRARY_PATH
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
"""),
'setup_env': ('setup_env.sh', """
#!/bin/bash
# sets up environment for your own work.
# in this case we can't use dirname, because this one is supposed to
# be sourced.
MYDIR=%s
source $MYDIR/paths.inc

export PYTHONPATH
export LD_LIBRARY_PATH
"""),
'devide' : ('devide.sh', """
#!/bin/bash
# invokes DeVIDE
MYDIR=`dirname $0`
source $MYDIR/paths.inc

export PYTHONPATH
export LD_LIBRARY_PATH

python $MYDIR/devide/devide.py $*
"""),

'python' : ('python.sh', """
#!/bin/bash
# invokes DeVIDE-capable Python
MYDIR=`dirname $0`
source $MYDIR/paths.inc

export PYTHONPATH
export LD_LIBRARY_PATH

python $*
""")
}

# we have to use %% where we want a single % due to the way python
# string interpolation works.  Python expects a single % to be
# followed by valid format specifiers.  Also see "Template strings"
# for a modern and simpler way to do string interpolation: 
# http://docs.python.org/lib/node40.html
nt_scripts = {'inc': ('paths.inc', """
@rem include file used by other DeVIDE scripts

@rem zero the pythonpath for this session
@set PYTHONPATH=

@rem wxpython
@set PATH=%(wx_lib_path)s;%%PATH%%

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
"""),
'setup_env': ('setup_env.cmd', """
"""),
'devide' : ('devide.cmd', """
"""),
'python' : ('python.cmd', """
""")
}

class SetupEnvironment(InstallPackage):

    def install(self):

        vardict = {'python_binary_path' : config.python_binary_path,
                   'python_library_path' : config.python_library_path,
                   'wx_lib_path' : config.WX_LIB_PATH,
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

        # replace all instances of the installation dir with the
        # variable $MYDIR / %MYDIR%
        vardict2 = {}
        idir = config.inst_dir
        if idir.endswith(os.path.sep):
            idir = idir[:-1]
            
        for k,v in vardict.items():
            vardict2[k] = v.replace(idir, '%(dre_top)s')

        print vardict2

        if os.name == 'nt':
            scripts = nt_scripts
            cfg = nt_cfg
        else:
            scripts = posix_scripts
            cfg = posix_cfg


        # let's write out the CFG file
        fname = os.path.join(config.inst_dir, 'dre.cfg')
        cf = file(fname, 'w')
        cfg2 = cfg % vardict2
        cf.write(cfg2)
        cf.close()
        utils.output('Write DRE CFG.')


        # will probably remove code below...
        return


        # create the paths include script text
        fname, inc_script = scripts['inc']
        inc_script = inc_script % vardict2
        # write it to disc
        inc_script_fn = os.path.join(config.inst_dir, 'paths.inc')
        sf = file(inc_script_fn, 'w')
        sf.write(inc_script)
        sf.close()
        utils.output('Wrote %s.' % (inc_script_fn,))

        # create the setup environment script text
        fname, setup_env_script = scripts['setup_env']
        setup_env_script = setup_env_script % (config.inst_dir,)
        # write it to disc
        se_script_fn = os.path.join(
                config.inst_dir, fname)
        sef = file(se_script_fn, 'w')
        sef.write(setup_env_script)
        sef.close()
        utils.output('Write %s.' % (se_script_fn,))

        fname, devide_script = scripts['devide']
        dsfn = os.path.join(
                config.inst_dir, fname)
        dsf = file(dsfn, 'w')
        dsf.write(devide_script)
        dsf.close()
        utils.output('Wrote %s.' % (dsfn,))

        fname, python_script = scripts['python']
        psfn = os.path.join(
                config.inst_dir, fname)
        psf = file(psfn, 'w')
        psf.write(python_script)
        psf.close()
        utils.output('Wrote %s.' % (psfn,))

    def get_installed_version(self):
        return None

