"""
Base plugin type
"""
import pluginTools

class PersonPlugin(pluginTools.Plugin):
    """
    Base plugin type
    """
    def __init__(self,name:str):
        self.name=name
        print(f'Hello, from {name}')
