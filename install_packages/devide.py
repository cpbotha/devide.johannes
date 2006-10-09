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
        

        script = """
#!/bin/bash
# invoke DeVIDE ###########################################
echo "Did you remember to run \". setup_env.sh\"?"
echo "Starting up DeVIDE..."
python %s --no-kits itk_kit,numpy_kit,matplotlib_kit $*
        """ % (config.DEVIDE_PY,)

        invoking_script_fn = os.path.join(config.working_dir, 'devide.sh')
        isf = file(invoking_script_fn, 'w')
        isf.write(script)
        isf.close()

        utils.output('Wrote %s.' % (invoking_script_fn,))

               
