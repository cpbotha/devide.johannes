# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.


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
        and onwards.
        """
        pass
