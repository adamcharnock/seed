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
            '-d', '--dry-run',
            dest='dry_run',
            action='store_true',
            default=False,
            help="Don't actually create anything, just show what will be created")

    def determine_paths(self, package_name=None, create_package_dir=False, dry_run=False):
        return super(CreateCommand, self).determine_paths(
            package_name=package_name, create_package_dir=True, dry_run=dry_run)
    
    def run(self, options, args):
        version = options.version
        
        self.dry_run = options.dry_run
        
        self.create_dirs()
        self.create_files(version)
        
        print("All done!")
        if not self.dry_run:
            print("You'll need to make some changes to setup.py (see comments in setup.py),")
            print("and putting something sensible in LICENSE.txt & README.rst ")
            print("is probably a good idea. You can optionally install 'check-manifest' ")
            print("to assist in creating a manifest if your packs includes static files.")

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
                    print("Would have created directory %s" % dir)
                else:
                    os.mkdir(dir, 0o755)
    
    def create_files(self, version):
        files = [
            (self.project_dir / "CHANGES.txt", TEMPLATE_CHANGES),
            (self.project_dir / "LICENSE.txt", TEMPLATE_LICENSE),
            (self.project_dir / "MANIFEST.in", TEMPLATE_MANIFEST),
            (self.project_dir / "VERSION", TEMPLATE_VERSION),
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
                    print("Would have created file %s" % file)
                else:
                    with open(file, "w+") as f:
                        f.write(content)
                    os.chmod(file, 0o644)
        
        if not self.dry_run:
            os.chmod(self.project_dir / "setup.py", 0o755)

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
include *.rst
recursive-include docs *
include VERSION
"""

TEMPLATE_README = """%(project_name)s
===========================================================

This readme has been autogenerated

.. image:: https://badge.fury.io/py/%(project_name)s.png
    :target: https://badge.fury.io/py/%(project_name)s

.. image:: https://pypip.in/d/%(project_name)s/badge.png
    :target: https://pypi.python.org/pypi/%(project_name)s

Installation
------------

Installation using pip::

    pip install %(project_name)s

Usage
-----

*Usage instructions here*

Credits
-------

*Any credits here*

%(project_name)s is packaged using seed_.

.. _seed: https://github.com/adamcharnock/seed/

"""

TEMPLATE_SETUP = """#!/usr/bin/env python

from os.path import exists
from setuptools import setup, find_packages

setup(
    name='%(project_name)s',
    version=open('VERSION').read().strip(),
    # Your name & email here
    author='',
    author_email='',
    # If you had %(package_name)s.tests, you would also include that in this list
    packages=find_packages(),
    # Any executable scripts, typically in 'bin'. E.g 'bin/do-something.py'
    scripts=[],
    # REQUIRED: Your project's URL
    url='',
    # Put your license here. See LICENSE.txt for more information
    license='',
    # Put a nice one-liner description here
    description='',
    long_description=open('README.rst').read() if exists("README.rst") else "",
    # Any requirements here, e.g. "Django >= 1.1.1"
    install_requires=[
        
    ],
    # Ensure we include files from the manifest
    include_package_data=True,
)
"""

TEMPLATE_INIT = ""

TEMPLATE_VERSION = "%(version)s"
