# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import utils
import shutil

BASENAME = "devide"
SVN_REPO = "http://devide.googlecode.com/svn/trunk/" + BASENAME
# this should be the same release as johannes and the rest of devide
SVN_REL = config.DEVIDE_REL

class DeVIDE(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.archive_dir, BASENAME)
        self.build_dir = os.path.join(config.build_dir, BASENAME)
        self.full_version = '%s.%s.0' % (SVN_REL, config.JOHANNES_REL)
        #self.inst_dir = os.path.join(config.inst_dir,
        #                             '%s-%s' % (BASENAME,
        #                                        self.full_version))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)

        # setup some devide config variables (we need to do this in anycase,
        # because they're config vars and other modules might want them)
        config.DEVIDE_PY = os.path.join(self.build_dir, 'devide.py')
        config.DEVIDE_MAKERELEASE_SH = os.path.join(
            self.build_dir, 'installer/makeRelease.sh')


    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("DeVIDE already checked out, skipping step.")

        else:
            os.chdir(config.archive_dir)
            ret = os.system("%s co %s -r%s" % (config.SVN, SVN_REPO, SVN_REL))
            if ret != 0:
                utils.error("Could not SVN checkout DeVIDE.  "
                            "Fix and try again.")

    def unpack(self):
        # we unpack by copying the checked out tree to the build dir
        if os.path.isdir(self.build_dir):
            utils.output(
                'DeVIDE already present in build dir.  Skipping step.')
            return

        shutil.copytree(self.source_dir, self.build_dir)

        # now modify the version unpacked devide.py
        devide_py = os.path.join(self.build_dir, 'devide.py')
        utils.re_sub_filter_file(
            [('(DEVIDE_VERSION\s*=\s*).*$', '\\1"%s.%s"' %
              (SVN_REL, config.JOHANNES_REL))],
            devide_py)

    def build(self):
        # first make script for starting DeVIDE right from the build dir
        # if the user wants to do so...
        ##################################################################
        script = """
#!/bin/bash
# invoke DeVIDE ###########################################
echo "Did you remember to run \". setup_env.sh\"?"
echo "Starting up DeVIDE..."
python %s $*

        """ % (config.DEVIDE_PY,)

        invoking_script_fn = os.path.join(config.working_dir, 'devide.sh')
        isf = file(invoking_script_fn, 'w')
        isf.write(script)
        isf.close()

        utils.output('Wrote %s.' % (invoking_script_fn,))

        # now also create script with which packages can be built
        #################################################################
        PYINSTALLER_SCRIPT = os.path.join(config.INSTALLER_DIR, 'Build.py')

        package_script = """
#!/bin/bash
echo "Did you remember to run \". setup_env.sh\"?"
export PYINSTALLER_SCRIPT=%s
sh %s package_only

        """ % (PYINSTALLER_SCRIPT, config.DEVIDE_MAKERELEASE_SH)

        ps_fn = os.path.join(config.working_dir, 'make_devide_package.sh')
        psf = file(ps_fn, 'w')
        psf.write(package_script)
        psf.close()

        utils.output('Wrote %s.' % (ps_fn,))

        # and then build the packages if the config says so
        ##################################################################
        if config.BUILD_DEVIDE_DISTRIBUTABLES:
            ddir = os.path.join(os.path.join(self.build_dir, 'installer'),
                                'distdevide')
            if os.path.isdir(ddir):
                utils.output('DeVIDE packages already built, skipping...')
                return
            
            ret = os.system(". %s && sh %s" %
                            (os.path.join(config.working_dir, 'setup_env.sh'),
                             ps_fn))
            
            if ret != 0:
                utils.error("Could not build DeVIDE installer packages.")
                return
            

    def install(self):
        if config.BUILD_DEVIDE_DISTRIBUTABLES:
            # check if devide has already been installed.
            if os.path.isdir(self.inst_dir):
                utils.output('DeVIDE already installed.  Skipping step.')
                return

            # we should have complete DeVIDE tarballs in devide/installer
            # and a complete (including ITK) installation in distdevide
            # copy binaries in distdevide to wd/inst/devide
            ddir = os.path.join(os.path.join(self.build_dir, 'installer'),
                                'distdevide')

            # we have to delete the destination path first
            # copytree doesn't work if the destination doesn't exist
            if os.path.isdir(self.inst_dir):
                shutil.rmtree(self.inst_dir)
                
            shutil.copytree(ddir, self.inst_dir)
                   
    def clean_build(self):
        utils.output("Removing build and installation directories.")

        if os.path.isdir(self.build_dir):
            shutil.rmtree(self.build_dir)

        if os.path.isdir(self.inst_dir):
            shutil.rmtree(self.inst_dir)
            
