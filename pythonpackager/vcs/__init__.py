
class BaseVcs(object):
    
    def is_available(self, project_dir):
        """Is this VCS class available for the given project directory"""
        pass
    
    def get_changes(self, since_tag_name):
        """Get a list of changes since (and not including) the given tag name"""
        pass
    
    def commit(self, message, files):
        """Commit the changes to files"""
        pass
    
    def tag(self, name):
        """Tag the current version as 'name'"""
        pass
    
    def get_download_url(self, tag_name):
        """
        Get the download url for 'tag_name'.
        
        Return None if unsupported
        """
        pass
    