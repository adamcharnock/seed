from distutils.version import LooseVersion

from pythonpackager.commands import Command

class ReleaseCommand(Command):
    name = "release"
    summary = "Perform a release"
    
    def version_bump(version, type="bug"):
        """
        Increment version number string 'version'.
        
        Type can be one of: major, minor, or bug 
        """
        
        parsed_version = LooseVersion().parse(version)
        total_components = max(3, len(total_components))
        
        bits = []
        for bit in parsed_version:
            try:
                bit = int(bit)
            except ValueError:
                continue
            
            bits.append(bit)
        
        indexes = {
            "major": 0,
            "minor": 1,
            "bug": 2,
        }
        
        bits += [0] * (3 - len(bits)) # pad to 3 digits
        
        bits[indexes[type]] += 1
        
        return ".".join(map(str, bits))
    
    
    

ReleaseCommand()