# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import config
from install_package import InstallPackage
import os
import utils
import shutil
import sys

BASENAME = "devide"
HG_REPO = "https://code.google.com/p/%s/" % (BASENAME,)
# this should be the same release as johannes and the rest of devide
CHANGESET_ID = config.DEVIDE_CHANGESET_ID

dependencies = []

class DeVIDE(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.archive_dir, BASENAME)
        self.build_dir = os.path.join(config.build_dir, BASENAME)
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)

        # setup some devide config variables (we need to do this in anycase,
        # because they're config vars and other modules might want them)
        config.DEVIDE_PY = os.path.join(self.inst_dir, 'devide.py')
        config.DEVIDE_INST_DIR = self.inst_dir
        config.DEVIDE_SRC_DIR = self.source_dir

    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("DeVIDE already checked out, skipping step.")

        else:
            os.chdir(config.archive_dir)
            ret = os.system("%s clone %s -u %s" % (config.HG, HG_REPO, CHANGESET_ID))
            if ret != 0:
                utils.error("Could not hg clone DeVIDE.  "
                            "Fix and try again.")

            # inject version information into devide.py
            utils.output("Modifying DeVIDE version.")
            devide_py = os.path.join(self.source_dir, 'devide.py')
           
            status, output = utils.get_status_output("%s id %s" % (config.HG, self.source_dir))
            # on linux, hg id gives "changeset_id tip" (e.g.)
            # on windows build image, only "changeset_id", so we have
            # to remove EOL with strip()
            devide_revision_id = output.split(' ')[0].strip()

            utils.re_sub_filter_file(
                [('(VERSION\s*=\s*)\"(.*)\"', '\\1"%s"' % (config.DEVIDE_DATESTR,)),
                 ('(DEVIDE_REVISION_ID\s*=\s*)\"(.*)\"', '\\1"%s"' % (devide_revision_id,)),
                 ('(JOHANNES_REVISION_ID\s*=\s*)\"(.*)\"', '\\1"%s"' % (config.JOHANNES_REVISION_ID,)),
                    ],
                devide_py)

    def unpack(self):
        """No unpack step.
        """
        pass

    def copy_devide_to_inst(self):
        # we unpack by copying the checked out tree to the build dir
        if os.path.isdir(self.inst_dir):
            utils.output(
                'DeVIDE already present in inst dir.  Skipping step.')
            return

        shutil.copytree(self.source_dir, self.inst_dir)



    def build(self):
        pass

    def install(self):
        self.copy_devide_to_inst()

    def clean_build(self):
        utils.output("Removing build and installation directories.")

        if os.path.isdir(self.inst_dir):
            shutil.rmtree(self.inst_dir)

    def get_installed_version(self):
        import sys
        sys.path.insert(0, self.inst_dir)
        import devide
        del sys.path[0]
        return devide.DEVIDE_VERSION


            
