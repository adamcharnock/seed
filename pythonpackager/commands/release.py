import os
import re
from path import path
import fileinput
import datetime

from distutils.version import LooseVersion

from pythonpackager.commands import Command
from pythonpackager.vcs import get_suitable_vcs

class ReleaseCommand(Command):
    name = "release"
    summary = "Perform a release"
    
    def __init__(self):
        super(CreateCommand, self).__init__()
        
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
            default="0.1.0",
            type='str',
            help='The new version number in the format x.y.z. Can also use --bug/--minor/--major to bump the current version number')
        
        self.parser.add_option(
            '--bug',
            dest='bug',
            action='store_true',
            default=False,
            type='str',
            help='This is a minor release (i.e. 0.0.1)')
        
        self.parser.add_option(
            '--minor',
            dest='minor',
            action='store_true',
            default=False,
            type='str',
            help='This is a minor release (i.e. 0.1.0)')
        
        self.parser.add_option(
            '--major',
            dest='major',
            action='store_true',
            default=False,
            type='str',
            help='This is a major release (i.e. 1.0.0)')
        
        self.parser.add_option(
            '-d', '--dry-run',
            dest='dry_run',
            action='store_true',
            default=False,
            help="Don't actually do anything, just show what will happen")
        
    
    def run(self, options, args):
        project_dir = path(os.getcwd())
        package_name = options.package_name
        package_dir = project_dir / package_name
        
        vcs = get_suitable_vcs()
        previous_version = self.read_version(package_dir)
        next_version = self.get_next_version(options, package_dir, previous_version)
        
        if options.dry_run:
            print "Version would be bumped to %s" % version
        else:
            self.write_version(package_dir, version)
        
        changes = vcs.get_changes(previous_version)
        if options.dry_run:
            print "Would have written %d changes to changelog" % changelog
        else:
            self.write_changelog(project_dir, changes, next_vesion)
        
        # Now do the commit
        
        # Now do the tag
        
        # Now do the push
        
        # Now update pypi
    
    def get_next_version(self, options, package_dir, previous_version):
        if options.release:
            return options.release
        
        if options.major: type = "major"
        if options.minor: type = "minor"
        if options.bug: type = "bug"
        
        return self.version_bump(version=previous_version, type)
    
    def read_version(self, package_dir):
        with open(package_dir / "__init__.py", "r") as f:
            # Read the first 1k - should be safe to assume the 
            # version is in there somewhere
            contents = f.read(1024)
        
        version = re.search(r"__version__ = ['\"](.*?)['\"]", contents).group(0)
        return version
    
    def write_version(self, package_dir, version):
        # This will captute STDOUT and overwrite the file
        for line in fileinput.input(package_dir / "__init__.py", inplace=1):
            # Don't forget your trailing commas (supresses extra new lines)
            if line.startswith("__version__ = "):
                print '__version__ = "%s"' % version,
            else:
                print line,
    
    def write_changelog(self, project_dir, changes, next_vesion):
        # This will captute STDOUT and overwrite the file
        written = False
        for line in fileinput.input(project_dir / "CHANGES.txt", inplace=1):
            print line,
            if not written and line.startswith("----"):
                written = True
                
                # Write our new log messages
                
                date = datetime.now().strftime("%a %d %b %Y")
                header = "\nVersion %s, %s" % (next_vesion, date)
                print "%s\n%s\n\n" % (header, "=" * len(header)),
                for commit, author, message in changes:
                    print "%s\t%s (%s)" % (commit, message, author)
                print "\n",
    
    def version_bump(self, version, type="bug"):
        """
        Increment version number string 'version'.
        
        Type can be one of: major, minor, or bug 
        """
        
        parsed_version = LooseVersion().parse(version)
        total_components = max(3, len(total_components))
        
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