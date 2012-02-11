
class CommandError(Exception): pass
class VcsCommandError(Exception): pass
class NoVcsError(Exception): pass

class ShellCommandError(Exception):
    
    def __init__(self, message, output, *args, **kwargs):
        super(ShellCommandError, self).__init__(message, *args, **kwargs)
        self.output = output
    
    def __str__(self):
        s = super(ShellCommandError, self).__str__()
        return "%s. Output was:\n%s" % (s, self.output.strip())