import config
from install_package import InstallPackage
import os
import utils

BASENAME = "devide"
SVN_REPO = "https://stockholm.twi.tudelft.nl/svn/devide/trunk/" + BASENAME

class DeVIDE(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.archive_dir, BASENAME)

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
        config.DEVIDE_MAKERELEASE_SH = os.path.join(
            self.source_dir, 'installer/makeRelease.sh')
        

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

               
    def clean_build(self):
        utils.output("Removing source directory.")
        if os.path.exists(self.source_dir):
            shutil.rmtree(self.source_dir)
            
