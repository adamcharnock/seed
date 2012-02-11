import optparse

parser = optparse.OptionParser(
    usage='%prog COMMAND [OPTIONS]',
    version="x.x.x",
    add_help_option=False)

parser.add_option(
    '-h', '--help',
    dest='help',
    action='store_true',
    help='Show help')

parser.disable_interspersed_args()

