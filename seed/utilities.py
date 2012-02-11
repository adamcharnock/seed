from subprocess import PIPE, STDOUT, Popen
from seed.exceptions import ShellCommandError

def run_command(command):
    p = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT, close_fds=True)
    captured = p.stdout.read()
    rc = p.poll()
    
    if rc:
        raise ShellCommandError("Command returned exit status %d: %s" % (rc, command), output=captured)
    
    return captured.strip()