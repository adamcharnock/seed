import sys

from pip.backwardcompat import walk_packages

vcs_dict = {}

def load_vcs(name):
    full_name = 'seed.vcs.%s' % name
    if full_name in sys.modules:
        return
    try:
        __import__(full_name)
    except ImportError:
        pass

def load_all_vcs():
    for name in vcs_names():
        load_vcs(name)

def vcs_names():
    from seed import vcs
    names = set((pkg[1] for pkg in walk_packages(path=vcs.__path__)))
    return list(names)

def get_suitable_vcs():
    load_all_vcs()
    possibilities = []
    for name, vcs in vcs_dict.items():
        possibilities.append((vcs.get_suitability(), vcs))
    
    best_score, best_vcs = sorted(possibilities, reverse=True)[0]
    
    if best_score <= 0:
        raise NoVcsError("No suitable VCS system seems to be active")
    
    return best_vcs

class BaseVcs(object):
    
    def __init__(self):
        vcs_dict[self.name] = self
    
    def is_available(self, project_dir):
        """Is this VCS class available for the given project directory"""
        pass
    
    def get_changes(self, since_version):
        """Get a list of changes since (and not including) the given version name
        
        Output should be in the format:
        [
            (commit, author, message),
            ...
        ]
        """
        pass
    
    def commit(self, message, files):
        """Commit the changes to files"""
        pass
    
    def tag(self, version):
        """Tag the current version as 'name'"""
        pass
    
    def get_download_url(self, version):
        """
        Get the download url for the given version.
        
        Return None if unsupported
        """
        pass
    
    def make_tag_name(self, version):
        return "v%s" % version
    