# Copyright (c) Charl P. Botha, TU Delft.
# All rights reserved.
# See COPYRIGHT for details.

import ConfigParser
from ConfigParser import NoOptionError
import config
import getopt
import os
import sys
import utils

def usage():
    message = """
Welcome to johannes, the ugliest
downloading/unpacking/configuring/building and installation system of
them all.  It could save you a lot of time though.  This instance of
johannes will get, build and install the following: python, numpy,
wxpython, matplotlib, cmake, dcmtk, vtk, vtktudoss, vtkdevide, itk,
itktudoss, itkvtkglue, devide

Please read the included README.txt file NOW.

Build method A (the default) is as follows: Before starting
johannes.py, first run bootstrap_stage1.sh and bootstrap_stage2.sh to
download and install python.  After that, run johannes as follows:

/you/new/python johannes.py -w working_directory

Options are as follows:
-w, --working-dir      : specify working directory [REQUIRED]
-h, --help             : show this help
-m, --mode             : working mode, 'everything' (default),
                         'clean_build', 'get_only' or 'configure_only'
-p, --install-packages : specify comma-separated list of packages to work on,
                         default all.  Example: -p "CMake,CableSwig"
                         Correct capitalisation IS important!
-d, --auto-deps        : Automatically build per install package dependencies.
                         The default is not to do this, i.e. you have to
                         specify all required packages on the command-line
                         or in the johannes.cfg project file.
--no-prereq-check      : do NOT do prerequisites check.
-v, --versions         : display installed versions of all packages.
-t, --target           : Specify a package to execute the 'mode' action on.
                         All build stages are performed on the non-target 
                         packages. Does not work for auto-deps.

You can also specify project-specific options (for example specifying
install packages) in a johannes.cfg file placed at the top-level
of your working directory.  See example-johannes.cfg for more info.

All of this ugliness is copyright 2006-2011 Charl P. Botha http://cpbotha.net/
and is hereby put under a BSD license.
"""

    print message

def posix_prereq_check(working_dir):
    """Perform posix system check for prerequisite software.

    Largest part of this checking is done in the second bootstrap
    shell script (executed before this file).  Here we check for basic
    stuff like cvs, svn and patch.
    """

    v = utils.find_command_with_ver(
            'CVS', '%s -v' % (config.CVS,),
            '\(CVS\)\s+(.*)\s+')

    v = v and utils.find_command_with_ver(
            'Subversion (SVN)', '%s --version' % (config.SVN,),
            'version\s+(.*)$')

    v = v and utils.find_command_with_ver(
            'patch', '%s -v' % (config.PATCH,),
            '^patch\s+(.*)$')

    # now check that working_dir contains the required subdirs
    dv = True
    for wsub in ['archive', 'build', 'inst']:
        cdir = os.path.join(working_dir, wsub)
        if os.path.isdir(cdir):
            msg = '%s exists.' % (cdir,)
        else:
            msg = '%s does not exist.' % (cdir,)
            dv = False

        utils.output(msg)

    return v and dv


def windows_prereq_check(working_dir):
    """Perform Windows system check for prerequisite software and
    directory structure.
    """

    utils.output("Windows prerequisites check", 70, '#')

    v = utils.find_command_with_ver(
            'MS Visual Studio', '%s /?' % (config.DEVENV,), 
            'Visual Studio Version (.*)\.$')

    #v = v and utils.find_command_with_ver(
    #        'CMake', '%s --version' % (config.CMAKE_BINPATH,),
    #        '^cmake version\s+(.*)$')

    v = v and utils.find_command_with_ver(
            'CVS', '%s -v' % (config.CVS,),
            '\((CVS|CVSNT)\)\s+(.*)\s+')

    v = v and utils.find_command_with_ver(
            'Subversion (SVN)', '%s --version' % (config.SVN,),
            'version\s+(.*)$')

    v = v and utils.find_command_with_ver(
            'GIT', '%s --version' % (config.GIT,),
            'version\s+(.*)$')

    v = v and utils.find_command_with_ver(
            'patch', '%s -v' % (config.PATCH,),
            '^patch\s+(.*)$')


    # now check that working_dir contains the required subdirs
    dv = True
    for wsub in ['archive', 'build', 'inst']:
        cdir = os.path.join(working_dir, wsub)
        if os.path.isdir(cdir):
            msg = '%s exists.' % (cdir,)
        else:
            msg = '%s does not exist.' % (cdir,)
            dv = False

        utils.output(msg)

    return v and dv


def main():

    if len(sys.argv) < 2:
        usage()

    else:
        rpad = 60
        rpad_char = '+'

        # this is the default list of install packages
        #
        # you can override this by:
        # - specifying packages on the johannes command line
        # - specifying packages in the working dir johannes.py
        # (command line has preference over config file)
        #
        # capitalisation has to match the capitalisation of your
        # install package class, name of install package module is
        # exactly that, but all lower case, so e.g. MyModule will
        # become: install_packages.ip_mymodule.MyModule()
        #
        # johannes will:
        # - attempt to import the ip_name from install_packages
        # - instantiate ip_name.Name
        #
        ip_names = [
                'pip',
                'NumPy',
                'WXPython',
                'matplotlib',
                'CMake',
                'DCMTK',
                'VTK56',
                'IPython',
                'VTKTUDOSS',
                'ITK',
                'SWIG',
                'CableSwig',
                'WrapITK',
                'ItkVtkGlue',
                'itkPyBuffer',
                'ITKTUDOSS',
                'GDCM',
                'DeVIDE',
                'VTKDEVIDE',
                'SetupEnvironment'
                ]




        try:
            optlist, args = getopt.getopt(
                sys.argv[1:], 'hm:p:dw:vt:',
                ['help', 'mode=', 'install-packages=', 
                    'auto-deps',
                    'working-dir=',
                    'no-prereq-check', 'versions'
                    'target='])

        except getopt.GetoptError,e:
            usage()
            return

        mode = 'everything'
        #ip_names = None
        working_dir = None
        profile = 'default'
        no_prereq_check = False
        ip_names_cli = False
        auto_deps = False
        target = None
        
        for o, a in optlist:
            if o in ('-h', '--help'):
                usage()
                return

            elif o in ('-m', '--mode'):
                if a in ('clean', 'clean_build'):
                    mode = 'clean_build'
                else:
                    mode = a

            elif o in ('--install-packages'):
                # list of package name to perform the action on
                ip_names = [i.strip() for i in a.split(',')]
                # remember that the user has specified ip_names on the command-line
                ip_names_cli = True

            elif o in ('-d', '--auto-deps'):
                auto_deps = True

            elif o in ('-w', '--working-dir'):
                working_dir = a

            elif o in ('--profile'):
                profile = a

            elif o in ('--no-prereq-check'):
                no_prereq_check = True

            elif o in ('-v', '--versions'):
                mode = 'show_versions'
                
            elif o in ('-t', '--target'):
                target = a

        # we need at LEAST a working directory
        if not working_dir:
            usage()
            return

        # init config (DURR)
        config.init(working_dir, profile)


        # set some variables we'll need to check later depending on
        # the configuration
        ip_dirs = []
        # now try to read johannes config file from the working dir
        cp = ConfigParser.ConfigParser()
        # returns list of filenames successfully parsed
        cfgfns = cp.read(os.path.join(working_dir, 'johannes.cfg'))
        if cfgfns and cp.has_section('default'):
            if not ip_names_cli:
                # first packages that need to be installed
                # we only do this if the user has NOT specified install
                # packages on the command line.
                try:
                    ip_names = [i.strip() 
                            for i in cp.get(
                                'default', 'packages').split(',')]
                except NoOptionError:
                    pass

            # also try to read extra install package paths
            # this is also a comma separated list
            try:
                ip_dirs = [i.strip()
                        for i in cp.get(
                            'default', 'ip_dirs').split(',')]
            except NoOptionError:
                pass

        # if user is asking for versions, we don't do the
        # prerequisites check as we're not going to build anything
        if mode == 'show_versions':
            no_prereq_check = True

        if os.name == 'nt' and not no_prereq_check:
            if not windows_prereq_check(working_dir):
                utils.output(
                     'Windows prerequisites do not check out.  '
                     'Fix and try again.', 70, '-')
                return
            else:
                utils.output(
                        'Windows prerequisites all good.', 70, '-')

        elif os.name == 'posix' and not no_prereq_check:
            if not posix_prereq_check(working_dir):
                utils.output(
                     'Posix prerequisites do not check out.  '
                     'Fix and try again.', 70, '-')
                return
            else:
                utils.output(
                        'Posix prerequisites all good.', 70, '-')

        # In case of a target, check whether the target is actually specified
        # in the ip list (does not check dependencies in case of auto-deps)
        if target != None:
            if not target in ip_names:
                utils.error("Target '%s' was not found in the install package list." % target)

        # we're going to do some imports, so let's set the sys.path
        # correctly.
        # 1. first the default install packages dir config.ip_dir
        sys.path.insert(0, config.ip_dir)

        # 2. insert the extra specified paths BEFORE that, so they get
        # preference
        for uip_dir in ip_dirs:
            sys.path.insert(0, uip_dir)

        # now import only the specified packages
        ip_instance_list = []
        imported_names = []

        def import_ip(ip_name):
            # don't import more than once
            if ip_name in imported_names:
                return

            # turn Name into ip_name
            ip_name_l = 'ip_' + ip_name.lower()
            # import the module, but don't instantiate the ip class yet
            ip_m = __import__(ip_name_l)

            # import dependencies first if user has specified
            # auto-deps.
            if auto_deps:
                for dep in ip_m.dependencies:
                    import_ip(dep)

            # instantiate ip_name.Name
            ip = getattr(ip_m, ip_name)()
            ip_instance_list.append(ip)
            imported_names.append(ip_name)
            print "%s imported from %s." % \
                    (ip_name, ip_m.__file__)

        # import all ip_names, including dependencies
        for ip_name in ip_names:
            import_ip(ip_name)

        # now check for dependencies and error if necessary
        # (in the case of auto_deps this will obviously be fine)
        deps_errors = []
        for ip in ip_instance_list:
            n = ip.__class__.__name__
            # there must be a more elegant way to get the module instance?
            deps = sys.modules[ip.__module__].dependencies
            for d in deps:
                # remember that if a package asks for "VTK", "VTK561" is also fine
                d_satisfied = False
                for ip_name in imported_names:
                    if ip_name.startswith(d):
                        d_satisfied = True
                        # we don't have to finish more loops
                        break

                    elif ip_name == n:
                        # this means we have reached the module whose deps
                        # we're checking without satisfying dependency d,
                        # which also means dependency problems, so we
                        # can jut break out of the for loop
                        break

                if not d_satisfied:
                    deps_errors.append('>>>>> Unsatisfied dependency: %s should be specified before %s' % (d, n))

        if deps_errors:
            print "\n".join(deps_errors)
            utils.error("Unsatisfied dependencies. Fix and try again.")

        def get_stage(ip, n):
            utils.output("%s :: get()" % (n,), rpad, rpad_char)
            ip.get()

        def unpack_stage(ip, n):
            utils.output("%s :: unpack()" % (n,), rpad, rpad_char)
            ip.unpack()

        def configure_stage(ip, n):
            utils.output("%s :: configure()" % (n,), rpad, rpad_char)
            ip.configure()

        def build_stage(ip, n):
            utils.output("%s :: build()" % (n,), rpad, rpad_char)
            ip.build()
            
        def install_stage(ip, n):
            utils.output("%s :: install()" % (n,), rpad, rpad_char)
            ip.install()
            
        def all_stages(ip, n):
            get_stage(ip, n)

            unpack_stage(ip, n)

            configure_stage(ip, n)            

            build_stage(ip, n)
            
            install_stage(ip, n)
            
        if mode == 'show_versions':
            utils.output('Extracting all install_package versions.')
            print "python: %d.%d.%d (%s)" % \
                    (sys.version_info[0:3] +
                            (config.PYTHON_EXECUTABLE,))
        
        for ip in ip_instance_list:
            n = ip.__class__.__name__
            
            if not n in ip_names:
                # n is a dependency, so do everything
                utils.output("%s (DEPENDENCY)" % (n,), 70, '#')
                all_stages(ip, n)
            
            elif target != None and target != n:
                # A target has been specified (but this ip is not it),
                # so do everything for all other install packages we encounter.
                utils.output("%s (NON-TARGET)" % (n,), 70, '#')
                all_stages(ip, n)
            
            elif mode == 'get_only':
                utils.output("%s GET_ONLY" % (n,), 70, '#')
                utils.output("%s" % (n,), 70, '#')
                get_stage(ip, n)

            elif mode == 'unpack_only':
                utils.output("%s UNPACK_ONLY" % (n,), 70, '#')
                utils.output("%s" % (n,), 70, '#')
                unpack_stage(ip, n)

            elif mode == 'configure_only':
                utils.output("%s CONFIGURE_ONLY" % (n,), 70, '#')
                utils.output("%s" % (n,), 70, '#')
                configure_stage(ip, n)

            elif mode == 'everything':
                utils.output("%s" % (n,), 70, '#')
                all_stages(ip, n)

            elif mode == 'clean_build':
                utils.output("%s CLEAN_BUILD" % (n,), 70, '#')
                ip.clean_build()

            elif mode == 'show_versions':
                print '%s: %s' % (n, ip.get_installed_version())
                
            elif mode == 'rebuild':
                utils.output("%s REBUILD" % (n,), 70, '#')
                # clean up
                ip.clean_build()
                # rebuild (executes all stages, as previous 
                # stages are required and user will likely 
                # need an install also)
                all_stages(ip, n)
                
            elif mode == 'reinstall':
                utils.output("%s REINSTALL" % (n,), 70, '#')
                # clean up
                ip.clean_install()
                # reinstall
                all_stages(ip, n)
                
            else:
                utils.output("%s CUSTOM MODE" % (n,), 70, '#')
                if hasattr(ip, mode):
                    utils.output("%s :: %s()" % (n, mode), rpad, rpad_char)                
                    getattr(ip, mode)()
                else:
                    utils.error("Mode not found: %s" % (mode,))
                
        if mode != 'show_versions':
            utils.output("Now please read the RESULTS section of README.txt!")

if __name__ == '__main__':
    main()
