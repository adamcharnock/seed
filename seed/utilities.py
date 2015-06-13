from subprocess import PIPE, STDOUT, Popen
from seed.exceptions import ShellCommandError

def run_command(command, ok_statuses=(0,)):
    p = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT, close_fds=True)
    captured = p.stdout.read().decode("utf-8")
    rc = p.wait()
    
    if rc not in ok_statuses:
        raise ShellCommandError("Command returned exit status %s: %s" % (rc, command), output=captured)

    return captured.strip()
