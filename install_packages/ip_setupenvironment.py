# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import shutil
import utils

dependencies = []

DRE_BASENAME = "dre"
HG_REPO = "https://code.google.com/p/devide.%s/" % (DRE_BASENAME,)
# this should be the same release as johannes and the rest of devide
CHANGESET_ID = config.DRE_CHANGESET_ID

posix_cfg = """
# DRE config written by johannes build system
# %%(dre_top)s will be replaced by the DRE top-level directory.

[env:path]
python: %(python_binary_path)s

[env:ld_library_path]
python: %(python_library_path)s
wxpython: %(wx_lib_path)s
vtk: %(vtk_sodir)s
gdcm: %(gdcm_lib)s
dcmtk: %(dcmtk_lib)s
vtkdevide: %(vtkdevide_lib)s
vtktudoss: %(vtktudoss_lib)s
itk: %(itk_lib)s:%(wrapitk_lib)s

[env:pythonpath]
devide: %(devide_inst_dir)s
vtk: %(vtk_python)s:%(vtk_sodir)s
gdcm: %(gdcm_python)s:%(gdcm_lib)s
vtkdevide: %(vtkdevide_python)s:%(vtkdevide_lib)s
vtktudoss: %(vtktudoss_python)s:%(vtktudoss_lib)s
itk: %(wrapitk_python)s:%(wrapitk_lib)s
"""

nt_cfg = """
# DRE config written by johannes build system
# %%(dre_top)s will be replaced by the DRE top-level directory.

[env:path]
python: %(python_binary_path)s
python_scripts: %(python_scripts_path)s
wxpython: %(wx_lib_path)s
vtk: %(vtk_sodir)s
gdcm: %(gdcm_lib)s
vtkdevide: %(vtkdevide_lib)s
vtktudoss: %(vtktudoss_lib)s
itk:%(itk_bin)s;%(wrapitk_lib)s

[env:pythonpath]
devide: %(devide_inst_dir)s
vtk: %(vtk_python)s;%(vtk_sodir)s
gdcm: %(gdcm_python)s;%(gdcm_lib)s
vtkdevide: %(vtkdevide_python)s;%(vtkdevide_lib)s
vtktudoss:%(vtktudoss_python)s;%(vtktudoss_lib)s
itk:%(wrapitk_python)s;%(wrapitk_lib)s

[env:pythonhome]
python: %(python_binary_path)s

"""

class SetupEnvironment(InstallPackage):

    def __init__(self):
        self.dre_src_dir = os.path.join(config.archive_dir, DRE_BASENAME)

        self.dreams_dest_dir = os.path.join(
                config.inst_dir, 'dreams')

        self.drepy_src = os.path.join(
                self.dre_src_dir, 'core', 'dre.py')
        self.drepy_dest = os.path.join(
                config.inst_dir, 'dre.py')

        if os.name == 'nt':
            shfn = 'dre.cmd'
            shpyfn = 'drepython.cmd'
        else:
            shfn = 'dre'
            shpyfn = 'drepython'

        self.dresh_src = os.path.join(
                self.dre_src_dir, 'core', shfn)
        self.dreshpy_src = os.path.join(
                self.dre_src_dir, 'core', shpyfn)
        self.dresh_dest = os.path.join(
                config.inst_dir, shfn)
        self.dreshpy_dest = os.path.join(
                config.inst_dir, shpyfn)

    def get(self):
        if os.path.exists(self.dre_src_dir):
            utils.output("DRE already checked out, skipping step.")

        else:
            os.chdir(config.archive_dir)
            ret = os.system("%s clone %s -u %s %s" % (config.HG, HG_REPO, CHANGESET_ID, DRE_BASENAME))
            if ret != 0:
                utils.error("Could not hg clone DRE.  "
                            "Fix and try again.")


    def install(self):

        # copy dreams dir and relevant driver scripts to inst dir
        if os.path.exists(self.dreams_dest_dir):
            utils.output('DREAMs already in inst_dir, not copying.')
        else:
            shutil.copytree(
                    os.path.join( self.dre_src_dir, 'dreams'),
                    self.dreams_dest_dir)
            utils.output('Copied %s.' % (self.dreams_dest_dir,))

        driver_paths = ((self.drepy_src, self.drepy_dest), (self.dresh_src, self.dresh_dest),
                        (self.dreshpy_src, self.dreshpy_dest))

        for d in driver_paths:
            if os.path.exists(d[1]):
                utils.output('%s already present.' % (d[1],))
            else:
                shutil.copy2(d[0], d[1])
                utils.output('Copied %s.' % (d[1],))
        
        vardict = {'python_binary_path' : config.python_binary_path,
                   'python_library_path' : config.python_library_path,
                   'python_scripts_path' : config.python_scripts_path,
                   'devide_inst_dir' : config.DEVIDE_INST_DIR,
                   'wx_lib_path' : config.WX_LIB_PATH,
                   'vtk_sodir' : config.VTK_SODIR,
                   'vtk_python' : config.VTK_PYTHON,
                   'dcmtk_lib' : config.DCMTK_LIB,
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

        if os.name == 'nt':
            cfg = nt_cfg
        else:
            cfg = posix_cfg

        # let's write out the CFG file
        fname = os.path.join(config.inst_dir, 'dre.cfg')
        cf = file(fname, 'w')
        cfg2 = cfg % vardict2
        cf.write(cfg2)
        cf.close()
        utils.output('Write DRE CFG.')

        # and then we have to fix all of the shebangs that distutils sets as absolute paths!
        if os.name == 'posix':
            pyscripts = utils.find_files(config.python_binary_path, 
                    '.*', exclude_pats=['python$','python[0-9]\.[0-9]$'])[0]
            
            for pyscript in pyscripts:
                utils.re_sub_filter_file([('#!.*', '#!/usr/bin/env python')], pyscript)


    def get_installed_version(self):
        return None

