import os
import os.path
from path import path

from seed.exceptions import CommandError
from seed.commands import Command

class CreateCommand(Command):
    name = "create"
    summary = "Create a skeleton package in the current directory"
    
    def __init__(self):
        super(CreateCommand, self).__init__()
        
        self.parser.add_option(
            '-r', '--release',
            dest='version',
            action='store',
            default="0.1.0",
            type='str',
            help='The initial release version. Default is 0.1.0')
        
        self.parser.add_option(
            '-f', '--force',
            dest='force',
            action='store_true',
            default=False,
            help='Force creation even if current directory is not empty.')
        
        self.parser.add_option(
            '-d', '--dry-run',
            dest='dry_run',
            action='store_true',
            default=False,
            help="Don't actually create anything, just show what will be created")
    
    def run(self, options, args):
        version = options.version
        
        self.dry_run = options.dry_run
        
        if not options.force and os.listdir(self.project_dir):
            raise CommandError("Project directory %s is not empty. Use -f for force.")
        
        self.create_dirs()
        self.create_files(version)
        
        print "All done!"
        if not self.dry_run:
            print "You'll need to make some changes to setup.py (see the comments),"
            print "and putting something sensible in LICENSE.txt & README.rst "
            print "is probably a good idea."
    
    def create_dirs(self):
        dirs = [
            self.project_dir / "bin", 
            self.project_dir / "docs", 
            self.package_name,
        ]
        
        for dir in dirs:
            if os.path.isdir(dir):
                continue
            elif os.path.exists(dir):
                raise CommandError("File %s exists and is not a directory" % dir)
            else:
                if self.dry_run:
                    print "Would have created directory %s" % dir
                else:
                    os.mkdir(dir, 0755)
    
    def create_files(self, version):
        files = [
            (self.project_dir / "CHANGES.txt", TEMPLATE_CHANGES),
            (self.project_dir / "LICENSE.txt", TEMPLATE_LICENSE),
            (self.project_dir / "MANIFEST.in", TEMPLATE_MANIFEST),
            (self.project_dir / "README.rst", TEMPLATE_README),
            (self.project_dir / "setup.py", TEMPLATE_SETUP),
            (self.package_dir / "__init__.py", TEMPLATE_INIT),
        ]
        
        for file, template in files:
            if os.path.isfile(file):
                continue
            elif os.path.exists(file):
                raise CommandError("File %s exists and is not a regular file" % dir)
            else:
                content = template % {
                    "project_name": self.project_name,
                    "package_name": self.package_name,
                    "version": version,
                }
                
                if self.dry_run:
                    print "Would have created file %s" % file
                else:
                    with open(file, "w+") as f:
                        f.write(content)
                    os.chmod(file, 0644)
        
        if not self.dry_run:
            os.chmod(self.project_dir / "setup.py", 0755)

CreateCommand()

TEMPLATE_CHANGES = """Change-log for %(project_name)s.

This file will be added to as part of each release

----
"""

TEMPLATE_LICENSE = """Put your license in this file

A list of many open source licenses can be found here:
http://www.opensource.org/licenses/category
"""

TEMPLATE_MANIFEST = """include *.txt
recursive-include docs *"""

TEMPLATE_README = """Auto generated readme file for %(project_name)s.

Put something informative here"""

TEMPLATE_SETUP = """from distutils.core import setup
from %(package_name)s import __version__

setup(
    name='%(project_name)s',
    version=__version__,
    # Your name & email here
    author='',
    author_email='',
    # If you had %(package_name)s.tests, you would also include that in this list
    packages=['%(package_name)s'],
    # Any executable scripts, typically in 'bin'. E.g 'bin/do-something.py'
    scripts=[],
    # REQUIRED: Your project's URL
    url='',
    # Put your license here. See LICENSE.txt for more information
    license='',
    # Put a nice one-liner description here
    description='',
    long_description=open('README.rst').read(),
    # Any requirements here, e.g. "Django >= 1.1.1"
    install_requires=[
        
    ],
)
"""

TEMPLATE_INIT = """__version__ = '%(version)s'
"""