import optparse
import sys
import difflib
import os

from path import path
from pip.backwardcompat import walk_packages

from seed.baseparser import parser
from seed.exceptions import CommandError

command_dict = {}

def load_command(name):
    full_name = 'seed.commands.%s' % name
    if full_name in sys.modules:
        return
    try:
        __import__(full_name)
    except ImportError:
        pass

def load_all_commands():
    for name in command_names():
        load_command(name)

def command_names():
    from seed import commands
    names = set((pkg[1] for pkg in walk_packages(path=commands.__path__)))
    return list(names)

class Command(object):
    name = None
    usage = None
    hidden = False

    def __init__(self):
        assert self.name
        self.parser = optparse.OptionParser(
            usage=self.usage,
            prog='%s %s' % (sys.argv[0], self.name),
            version=parser.version)
        for option in parser.option_list:
            if not option.dest or option.dest == 'help':
                # -h, --version, etc
                continue
            self.parser.add_option(option)
        
        command_dict[self.name] = self
        
        self.parser.add_option(
            '-n', '--name',
            dest='package_name',
            action='store',
            default='',
            type='str',
            help='The package name. Will try to auto-detect if possible.')
    
    def main(self, args, initial_options):
        options, args = self.parser.parse_args(args)
        
        # TODO: Pull options for env or settings file (currently ignoring initial_options)
        # TODO: Catch exceptions from command.run()
        # TODO: Setup logging in some way
        
        self.determine_paths(options.package_name)
        
        self.run(options, args)
    
    def determine_paths(self, package_name=None):
        """Determine paths automatically and a little intelligently"""
        
        # Give preference to the environment variable here as it will not 
        # derefrence sym links
        self.project_dir = path(os.getenv('PWD') or os.getcwd())
        self.project_name = self.project_dir.name
        
        if package_name:
            self.package_name = package_name
        else:
            # Try and work out the package name
            possibles = [n for n in os.listdir(self.project_dir) if os.path.isdir(self.project_dir / n)]
            close = difflib.get_close_matches(self.project_name, possibles, n=1, cutoff=0.8)
            
            if not close:
                raise CommandError("Could not guess the package name. Specify it using --name.")
            
            self.package_name = close[0]
        
        self.package_dir = self.project_dir / self.package_name
    

