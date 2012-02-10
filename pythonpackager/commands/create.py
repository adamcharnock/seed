from pythonpackager.commands import Command

class CreateCommand(Command):
    name = "create"
    
    def __init__(self):
        super(CreateCommand, self).__init__()
        self.parser.add_option(
            '-m', '--moo',
            dest='moo',
            action='store',
            default=None,
            type='str',
            help='Use the given requirements file as a hint about how to generate the new frozen requirements')
    
    def run(self, options, args):
        import pdb; pdb.set_trace();
        

CreateCommand()