import sys

from pip.backwardcompat import walk_packages

from seed.baseparser import parser
from seed.commands import load_command, command_dict

__version__ = "0.2.1"

def version_control():
    # Import all the version control support modules:
    from seed import vcs
    for importer, modname, ispkg in \
            walk_packages(path=vcs.__path__, prefix=vcs.__name__+'.'):
        __import__(modname)

def main(initial_args=None):
    if initial_args is None:
        initial_args = sys.argv[1:]
    version_control()
    options, args = parser.parse_args(initial_args)
    if options.help and not args:
        args = ['help']
    if not args:
        parser.error('You must give a command (use "help" to see a list of commands)')
    command = args[0].lower()
    load_command(command)
    if command not in command_dict:
        parser.error('No command by the name %s\n  ' % command)
    command = command_dict[command]
    return command.main(args[1:], options)


if __name__ == '__main__':
    exit = main()
    if exit:
        sys.exit(exit)
