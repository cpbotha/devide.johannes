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

    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("DeVIDE already checked out, skipping step.")

        else:
            # we're checking out a version of DeVIDE that matches the version
            # of DeVIDE. SVN_REL = DEVIDE_REL = JOHANNES_REL
            os.chdir(config.archive_dir)
            ret = os.system("%s clone %s -u %s" % (config.HG, HG_REPO, CHANGESET_ID))
            if ret != 0:
                utils.error("Could not hg clone DeVIDE.  "
                            "Fix and try again.")

            # now modify the version unpacked devide.py
            # we have to do this, because we've checked out SVN_REL
            # which is DEVIDE_REL which is JOHANNES_REL, but devide's
            # built-in SVN version could be different, because it was
            # not stamped. We want the DeVIDE version number in the
            # shipping software to reflect the johannes version that
            # builds it all.
            utils.output("Modifying DeVIDE version to reflect that of johannes.")
            devide_py = os.path.join(self.source_dir, 'devide.py')
            # we want to change DEVIDE_VERSION = '%s.%s' % (VERSION,
            # SVN_REVISION) to DEVIDE_VERSION = '%s.%s' % (VERSION,
            # "$JOHANNES_REL") 
            
            # FIXME: update for mercurial setup
            # we have config.DEVIDE_CHANGESET_ID
            # and we could get the changeset id of this johannes checkout as well.
            
            #utils.re_sub_filter_file(
            #    [('(DEVIDE_VERSION\s*=.*)SVN_REVISION(.*)', '\\1"%s"\\2' %
            #      (config.JOHANNES_REL,))],
            #    devide_py)

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
        config.DEVIDE_INST_DIR = self.inst_dir
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


            
