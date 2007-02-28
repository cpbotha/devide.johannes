import config
from install_package import InstallPackage
import os
import utils
import shutil

BASENAME = "devide"
SVN_REPO = "https://stockholm.twi.tudelft.nl/svn/devide/trunk/" + BASENAME
SVN_REL = "2435"

class DeVIDE(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.archive_dir, BASENAME)

    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("DeVIDE already checked out, skipping step.")

        else:
            os.chdir(config.archive_dir)
            ret = os.system("%s co %s -r%s" % (config.SVN, SVN_REPO, SVN_REL))
            if ret != 0:
                utils.error("Could not SVN checkout DeVIDE.  "
                            "Fix and try again.")

    def install(self):
        # setup some devide config variables
        config.DEVIDE_PY = os.path.join(self.source_dir, 'devide.py')
        config.DEVIDE_MAKERELEASE_SH = os.path.join(
            self.source_dir, 'installer/makeRelease.sh')
        

        # first make script for starting DeVIDE right from the archive dir
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

        # and then build the packages
        ##################################################################
        ret = os.system(". %s && sh %s" %
                        (os.path.join(config.working_dir, 'setup_env.sh'),
                         ps_fn))
        if ret != 0:
            utils.error("Could not build DeVIDE installer packages.")
            return

        # we should have complete DeVIDE tarballs in devide/installer
        # and a complete (including ITK) installation in distdevide
        # copy binaries in distdevide to wd/inst/devide
        ddir = os.path.join(os.path.join(self.source_dir, 'installer'),
                            'distdevide')
        devide_destdir = os.path.join(config.inst_dir, 'devide')
        # we have to delete the destination path first
        # copytree doesn't work if the destination doesn't exist
        shutil.rmtree(devide_destdir)
        shutil.copytree(ddir, devide_destdir)
               
    def clean_build(self):
        utils.output("Removing source directory.")
        if os.path.exists(self.source_dir):
            shutil.rmtree(self.source_dir)
            
