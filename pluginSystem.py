"""
A general plugin system
"""
import typing
from .plugin import Plugin


class PluginSystem:
    """
    A general plugin system
    """

    def registerPlugin(self,
        plugin:Plugin,
        context:typing.Optional[typing.Any]=None
        )->None:
        """
        Register a plugin with this system.

        :context: something that makes sense only to this plugin system,
            for instance a spellchecker plugin might want to register
            with a text editor to be invoked specifically when
            a word changes.

        NOTE: one plugin may call RegisterPlugin several times.
        """

    #def unRegisterPlugin(self,)


def registerPlugin(
    plugin:Plugin,
    system:PluginSystem,
    context:typing.Optional[typing.Any]=None):
    """
    Register a plugin with a system.

    :context: something that makes sense only to this plugin system,
        for instance a spellchecker plugin might want to register
        with a text editor to be invoked specifically when
        a word changes.

    NOTE: one plugin may call RegisterPlugin several times for a single system.
    """

def unRegisterPlugin(
    plugin:Plugin,
    system:PluginSystem,
    context:typing.Optional[typing.Any]=None):
    """
    unregister a plugin if it is going away
    """

def findAllPlugins(forSystem:PluginSystem):
    """
    find all plugins for a system
    """
    # help("modules") # everybody online says this works.  They lied.
    import pip
    print(dir(pip.main))
    for pkg in pip.get_installed_distributions(local_only=True):
        print(pkg)

findAllPlugins(None)
