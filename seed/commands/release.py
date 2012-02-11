import os
import re
import sys
from path import path
import fileinput
from datetime import datetime

from distutils.version import LooseVersion

from seed.commands import Command
from seed.utilities import run_command
from seed.exceptions import ShellCommandError, CommandError
from seed.vcs import get_suitable_vcs

class ReleaseCommand(Command):
    name = "release"
    summary = "Perform a release"
    
    def __init__(self):
        super(ReleaseCommand, self).__init__()
        
        default_name = path(os.getcwd()).name.lower().replace("-", "")
        
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
            help='This is a minor release (i.e. 0.0.1). This is the default.')
        
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
        
        self.parser.add_option(
            '-g', '--register',
            dest='register',
            action='store_true',
            default=False,
            help="Force the package to be registered with PyPi.")
        
        self.parser.add_option(
            '-p', '--push',
            dest='push',
            action='store_true',
            default=False,
            help="Push changes when complete (for distributed VCS only)")
        
    
    def run(self, options, args):
        vcs = get_suitable_vcs()
        previous_version = self.read_version()
        
        if not previous_version:
            raise CommandError("Could not determine version. Make sure your root __init__.py file contains '__version__ = \"1.2.3\"'")
        
        if options.initial:
            # We don't increment the version number for the initial commit
            next_version = previous_version
        else:
            next_version = self.get_next_version(options, previous_version)
        
        print "This release will be version %s" % next_version
        
        # Running checks
        print "Running package sanity checks on setup.py"
        output = run_command("python setup.py check")
        warnings = [l.split("check: ")[1] for l in output.split("\n") if "check: " in l]
        if warnings:
            print "Checks on setup.py failed. Messages were:\n%s" % "\n".join(warnings)
            sys.exit(1)
        
        # Update the version number
        
        if options.dry_run:
            print "Version would be set to %s" % next_version
        else:
            print "Version written"
            self.write_version(next_version)
        
        # Update the changelog
        
        if options.dry_run:
            if options.initial:
                print "Would have written the initial version to the changelog"
            else:
                changes = vcs.get_changes(previous_version)
                print "Would have written %d changes to changelog" % len(changes)
        else:
            print "Updating changelog"
            if options.initial:
                self.write_changelog([], "%s (first version)" % next_version)
            else:
                changes = vcs.get_changes(previous_version)
                self.write_changelog(changes, next_version)
        
        # Commit the changes we have made
        
        commit_files = [self.project_dir / "CHANGES.txt", self.package_dir / "__init__.py"]
        if options.dry_run:
            print "Would have committed changes to: %s" % ", ".join(commit_files)
        else:
            print "Committing changes"
            vcs.commit("Version bump to %s and updating CHANGES.txt" % next_version, commit_files)
        
        # Now do the tag
        if options.dry_run:
            print "Would have created a tag for version %s" % next_version
        else:
            print "Tagging new version"
            vcs.tag(next_version)
        
        if options.push and hasattr(vcs, "push"):
            if options.dry_run:
                print "Would have pushed changes"
            else:
                print "Pushing changes"
                vcs.push()        
        
        # Now register/upload the package
        if options.dry_run:
            print "Would have updated PyPi"
        else:
            print "Uploading to PyPi"
            print "(This may take a while, grab a cuppa. You've done a great job!)"
            if options.initial or options.register:
                run_command("python setup.py register sdist upload")
            else:
                run_command("python setup.py sdist upload")
        
        print "All done!"
        if not options.dry_run:
            print "We have made changes, but not pushed. Git users should probably do: "
            print "    git push --tags"
    
    def get_next_version(self, options, previous_version):
        if options.version:
            return options.version
        
        if options.major: type = "major"
        elif options.minor: type = "minor"
        elif options.bug: type = "bug"
        else: type = "bug"
        
        return self.version_bump(previous_version, type)
    
    def read_version(self):
        with open(self.package_dir / "__init__.py", "r") as f:
            # Read the first 1k - should be safe to assume the 
            # version is in there somewhere
            contents = f.read(1024)
        
        matches = re.search(r"__version__\s+=\s+['\"](.*?)['\"]", contents)
        
        if matches:
            return matches.group(1)
        else:
            return None
    
    def write_version(self, version):
        # This will captute STDOUT and overwrite the file
        for line in fileinput.input(self.package_dir / "__init__.py", inplace=1):
            if line.startswith("__version__ = "):
                print '__version__ = "%s"' % version
            else:
                print line,
    
    def write_changelog(self, changes, next_version):
        changelog = self.project_dir / "CHANGES.txt"
        
        # Create the file if it doesn't exist
        if not os.path.exists(changelog) or os.path.getsize(changelog) == 0:
            with open(changelog, "w+") as f:
                f.write("----\n")
        
        # This will captute STDOUT and overwrite the file
        written = False
        for line in fileinput.input(changelog, inplace=1):
            print line,
            if not written and line.startswith("----"):
                # Write our new log messages
                written = True
                print self.make_changelog_text(changes, next_version)
        
        if not written:
            # Didn't write anything, so lets just append it now
            with open(changelog, "a") as f:
                f.write("----\n")
                f.write(self.make_changelog_text())
        

    
    def make_changelog_text(self, changes, next_version):
        text = ""
        
        date = datetime.now().strftime("%a %d %b %Y")
        header = "\nVersion %s, %s" % (next_version, date)
        text += "%s\n%s\n\n" % (header, "=" * len(header))
        for commit, author, message in changes:
            text += "%s\t%s (%s)\n" % (commit, message, author)
        return text
    
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
        
        # Increment the version
        bits[indexes[type]] += 1
        
        # Set the subsequent digits to 0
        for i in range(indexes[type] + 1, 3):
            bits[i] = 0
        
        return ".".join(map(str, bits))
    
    
    

ReleaseCommand()