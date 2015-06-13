import re

from seed.utilities import run_command
from seed.vcs.git import GitVcs
from seed.exceptions import VcsCommandError

GH_DOWNLOAD_URL = "http://github.com/%s/%s/tarball/%s"

class GitHubVcs(GitVcs):
    name = "github"
    
    def get_suitability(self):
        try:
            self.get_user_repo()
        except VcsCommandError:
            print("It looks like this is a GitHub project, but we cannot "\
                  "determine a suitable remote because you have more than "\
                  "one GitHub remote url and none of them are called 'origin'.")
            return 0
        
        return 2
    
    def get_user_repo(self):
        # Get all remote urls
        output = run_command("git config --get-regexp 'remote\..*\.url'", ok_statuses=(0, 1))
        urls = {}
        for line in output.split("\n"):
            matches = re.match(r'remote\.(.*)\.url\s+(.*github\.com.*)', line)
            if matches:
                remote_name, url = matches.groups()
                urls[remote_name] = url
        
        if "origin" in urls:
            url = urls["origin"]
        elif len(urls) == 1:
            url = list(urls.values())[0]
        else:
            raise VcsCommandError("Could not determine a suitable GitHub remote url. "
                                  "This is because you have more than one GitHub remote url "
                                  "and none of them are called 'origin'.")
        
        # Parse out into user & repo
        return re.search(r"([a-z0-9-_]+)/([a-z0-9-_]+)", url).groups()
    
    def get_download_url(self, version):
        tag_name = self.make_tag_name(version)
        user, repo = self.get_user_repo()
        return GH_DOWNLOAD_URL % (user, repo, tag_name)
    

GitHubVcs()
