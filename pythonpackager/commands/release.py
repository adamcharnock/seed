import os
import re
from path import path
import fileinput
from datetime import datetime

from distutils.version import LooseVersion

from pythonpackager.commands import Command
from pythonpackager.utilities import run_command
from pythonpackager.exceptions import ShellCommandError
from pythonpackager.vcs import get_suitable_vcs

class ReleaseCommand(Command):
    name = "release"
    summary = "Perform a release"
    
    def __init__(self):
        super(ReleaseCommand, self).__init__()
        
        default_name = path(os.getcwd()).name.lower().replace("-", "")
        
        self.parser.add_option(
            '-n', '--name',
            dest='package_name',
            action='store',
            default=default_name,
            type='str',
            help='The package name. Will default to the current directory name, lower cased, and with dashes stripped.')
        
        self.parser.add_option(
            '-r', '--release',
            dest='version',
            action='store',
            default="",
            type='str',
            help='The new version number in the format x.y.z. Can also use --bug/--minor/--major to bump the current version number')
        
        self.parser.add_option(
            '--bug',
            dest='bug',
            action='store_true',
            default=False,
            help='This is a minor release (i.e. 0.0.1)')
        
        self.parser.add_option(
            '--minor',
            dest='minor',
            action='store_true',
            default=False,
            help='This is a minor release (i.e. 0.1.0)')
        
        self.parser.add_option(
            '--major',
            dest='major',
            action='store_true',
            default=False,
            help='This is a major release (i.e. 1.0.0)')
        
        self.parser.add_option(
            '-d', '--dry-run',
            dest='dry_run',
            action='store_true',
            default=False,
            help="Don't actually do anything, just show what will happen")
        
        self.parser.add_option(
            '-i', '--initial',
            dest='initial',
            action='store_true',
            default=False,
            help="This is the first release. Register this package with PyPi, don't increment the version number, don't write changes to the changelog")
    
    def run(self, options, args):
        project_dir = path(os.getcwd())
        package_name = options.package_name
        package_dir = project_dir / package_name
        
        vcs = get_suitable_vcs()
        previous_version = self.read_version(package_dir)
        if options.initial:
            # We don't increment the version number for the initial commit
            next_version = previous_version
        else:
            next_version = self.get_next_version(options, package_dir, previous_version)
        
        # Running checks
        try:
            run_command("python setup.py check")
        except ShellCommandError, e:
            print "Checks failed. Messages were:\n%s" % e.output
            sys.exit(1)
        
        # Update the version number
        
        if options.dry_run:
            print "Version would be set to %s" % next_version
        else:
            self.write_version(package_dir, next_version)
        
        # Update the changelog
        
        changes = vcs.get_changes(previous_version)
        if options.dry_run:
            if options.initial:
                print "Would have written the initial version to the changelog"
            else:
                print "Would have written %d changes to changelog" % len(changes)
        else:
            if options.initial:
                self.write_changelog(project_dir, changes, "%s (first version)" % next_version)
            else:
                self.write_changelog(project_dir, changes, next_version)
        
        # Commit the changes we have made
        
        commit_files = [project_dir / "CHANGES.txt", package_dir / "__init__.py"]
        if options.dry_run:
            print "Would have committed changes to: %s" % ", ".join(commit_files)
        else:
            vcs.commit("Version bump to %s and updating CHANGES.txt" % next_version, commit_files)
        
        # Now do the tag
        if options.dry_run:
            print "Would have created a tag for version %s" % next_version
        else:
            vcs.tag(next_version)
        
        # Now register the package (if this is the initial version)
        if options.dry_run:
            print "Would have updated PyPi"
        else:
            if options.initial:
                run_command("python setup.py register sdist upload")
            else:
                run_command("python setup.py sdist upload")
        
        print "All done! (we have made changes, but not pushed)"
    
    def get_next_version(self, options, package_dir, previous_version):
        if options.version:
            return options.version
        
        if options.major: type = "major"
        elif options.minor: type = "minor"
        elif options.bug: type = "bug"
        else: type = "bug"
        
        return self.version_bump(previous_version, type)
    
    def read_version(self, package_dir):
        with open(package_dir / "__init__.py", "r") as f:
            # Read the first 1k - should be safe to assume the 
            # version is in there somewhere
            contents = f.read(1024)
        
        version = re.search(r"__version__ = ['\"](.*?)['\"]", contents).group(1)
        return version
    
    def write_version(self, package_dir, version):
        # This will captute STDOUT and overwrite the file
        for line in fileinput.input(package_dir / "__init__.py", inplace=1):
            if line.startswith("__version__ = "):
                print '__version__ = "%s"' % version
            else:
                print line,
    
    def write_changelog(self, project_dir, changes, next_version):
        # This will captute STDOUT and overwrite the file
        written = False
        for line in fileinput.input(project_dir / "CHANGES.txt", inplace=1):
            print line,
            if not written and line.startswith("----"):
                written = True
                
                # Write our new log messages
                
                date = datetime.now().strftime("%a %d %b %Y")
                header = "\nVersion %s, %s" % (next_version, date)
                print "%s\n%s\n\n" % (header, "=" * len(header)),
                for commit, author, message in changes:
                    print "%s\t%s (%s)" % (commit, message, author)
                print "\n",
    
    def version_bump(self, version, type="bug"):
        """
        Increment version number string 'version'.
        
        Type can be one of: major, minor, or bug 
        """
        parsed_version = LooseVersion(version).version
        total_components = max(3, len(parsed_version))
        
        bits = []
        for bit in parsed_version:
            try:
                bit = int(bit)
            except ValueError:
                continue
            
            bits.append(bit)
        
        indexes = {
            "major": 0,
            "minor": 1,
            "bug": 2,
        }
        
        bits += [0] * (3 - len(bits)) # pad to 3 digits
        
        bits[indexes[type]] += 1
        
        return ".".join(map(str, bits))
    
    
    

ReleaseCommand()