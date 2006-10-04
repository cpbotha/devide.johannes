class InstallPackage:

    """All libraries that should be installed by johannes have to have
    InstallPackage abstractions.  This class defines which actions need to
    be taken to get, configure, build and install a complete library /
    software package.
    """

    def get():
        pass

    def unpack():
        pass

    def configure():
        pass

    def build():
        pass

    def install():
        pass
