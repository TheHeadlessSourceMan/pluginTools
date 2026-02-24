"""
Registered type of PersnPlugin
"""
from testPluginSystem import PersonPlugin

class Paul(PersonPlugin):
    """
    Registered type of PersnPlugin
    """
    def __init__(self):
        PersonPlugin.__init__(self,"Paul")
