# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import utils
import os
import shutil
import types

class InstallPackage:

    """All libraries that should be installed by johannes have to have
    InstallPackage abstractions.  This class defines which actions need to
    be taken to get, configure, build and install a complete library /
    software package.
    """

    def get(self):
        pass

    def unpack(self):
        pass

    def configure(self):
        pass

    def build(self):
        pass

    def install(self):
        pass

    def clean_build(self):
        """This method should clean up in such a way that the next build
        of this package will result in AT LEAST all steps from configure
        and onwards. By default, it removes the build dir and calls
        clean_install().
        """
        utils.output("Removing build and installation directories.")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        self.clean_install()
    
    def clean_install(self):
        """ Only cleans up the install directory.
        """
        utils.output("Removing installation directory.")
        if os.path.exists(self.inst_dir):
            shutil.rmtree(self.inst_dir)
    
    def list(self):
        """ Lists the methods of this install package.
           (Sometimes I forget what the exact names are)
        """
        atts = dir(self)
        for att in atts:
            if type(getattr(self, att)) == types.MethodType:
                utils.output(att)
    