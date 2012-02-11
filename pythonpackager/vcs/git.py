from pythonpackager.vcs import BaseVcs
from pythonpackager.utilities import run_command
from pythonpackager.exceptions import ShellCommandError

class GitVcs(BaseVcs):
    
    def is_available(self, project_dir):
        try:
            run_command("git status")
        except ShellCommandError:
            return False
        
        return True
    
    def get_changes(self, since_tag_name):
        pass
    
    def commit(self, message, files):
        pass
    
    def tag(self, name):
        pass
    
    def get_download_url(self, tag_name):
        pass
    