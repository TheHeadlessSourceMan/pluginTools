"""
A general plugin system

It is based upon pip packages
https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/#plugin-entry-points
"""
import typing
import importlib.metadata
from pluginTools.plugin import Plugin,SingletonPlugin


def getModuleNameOfObject(obj:object)->str:
    """
    Get the module name that an object belongs to
    """
    moduleName=obj.__module__
    if moduleName=='__main__':
        import inspect
        import paths
        filename=paths.Path(inspect.getfile(obj.__class__)).absolute()
        moduleName=filename.parent.name
    return moduleName


InstanceParamsType=typing.List[typing.Dict[str,typing.Any]]
InstancesParamsType=typing.Dict[str,InstanceParamsType]


PluginType=typing.TypeVar('PluginType',bound=Plugin)
class PluginSystem(typing.Generic[PluginType]):
    """
    A general plugin system
    """
    def __init__(self,
        pluginGroup:typing.Optional[str]=None):
        """
        :pluginGroup: the name of this plugin group.  If not specified,
            assumes it to be "[yourModule].plugin"
        """
        if pluginGroup is None:
            pluginGroup=getModuleNameOfObject(self)+'.plugin'
        self._pluginGroup=pluginGroup
        self._plugins:typing.Optional[typing.List[PluginType]]=None

    @property
    def pluginGroup(self)->str:
        """
        The name of this plugin group
        """
        return self._pluginGroup

    def findPlugins(self)->typing.Iterable[importlib.metadata.EntryPoint]:
        """
        Scan (but do not create instances of) all installed plugins that belong to this system
        """
        yield from findPlugins(self)

    def createPlugins(self,
        instancesParameters:typing.Optional[InstancesParamsType]=None
        )->typing.Iterable[PluginType]:
        """
        Scan, and create instances of, all installed plugins that belong to this system

        :instancesParameters: "pluginName":[{instande1_params},{instance2_params},{...}]
        """
        pluginGen=createPlugins(self,instancesParameters)
        pluginGen=typing.cast(typing.Generator[PluginType,None,None],pluginGen)
        self._plugins=list(pluginGen)
        return self._plugins
    refresh=createPlugins

    @property
    def plugins(self)->typing.Iterable[PluginType]:
        """
        All installed plugins that belong to this system.

        If new plugins have been installed since the last scan,
        you may need to refresh()
        """
        if self._plugins is None:
            self.refresh()
        return self._plugins # type: ignore

    def __iter__(self)->typing.Iterator[PluginType]:
        return iter(self.plugins)

    def __len__(self)->int:
        if self._plugins is None:
            self.refresh()
        return len(self._plugins) # type: ignore

    def registerPlugin(self,
        plugin:PluginType,
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

def findInstalledPackages(
    name:typing.Union[None,str,typing.Pattern]=None
    )->typing.Generator[importlib.metadata.Distribution,None,None]:
    """
    Find installed packages that match a given name
    """
    for distribution in importlib.metadata.distributions():
        if name is None:
            yield distribution
        elif isinstance(name,str):
            if name==distribution.name:
                yield distribution
        elif name.match(distribution.name):
            yield distribution


def findPlugins(
    pluginGroup:typing.Union[None,str,typing.Pattern,PluginSystem]=None
    )->typing.Generator[importlib.metadata.EntryPoint,None,None]:
    """
    Find installed plugins that match a given type
    """
    for package in findInstalledPackages():
        if not hasattr(package,'entry_points'):
            continue
        if pluginGroup is not None and isinstance(pluginGroup,PluginSystem):
            pluginGroup=pluginGroup.pluginGroup
        for entrypoint in package.entry_points:
            if pluginGroup is None:
                yield entrypoint
            elif isinstance(pluginGroup,str):
                if entrypoint.group==pluginGroup:
                    yield entrypoint
            elif pluginGroup.match(entrypoint.group):
                yield entrypoint


def createPlugins(
    pluginGroup:typing.Union[None,str,typing.Pattern,PluginSystem]=None,
    instancesParams:typing.Optional[InstancesParamsType]=None,
    printObjectInstanciation:bool=True
    )->typing.Generator[Plugin,None,None]:
    """
    Find installed plugins that match a given type
    and return an instance of each one.
    """
    if instancesParams is None:
        instancesParams={}
    for pluginInfo in findPlugins(pluginGroup):
        try:
            pluginClass=pluginInfo.load()
            if not issubclass(pluginClass,Plugin):
                raise TypeError(f'Expected class {Plugin}, got class {pluginClass}')
            instanceParams=instancesParams.get(pluginInfo.name,None)
            if instanceParams is None:
                if issubclass(pluginClass,SingletonPlugin):
                    # just because there are no params, doesn't mean we shouldn't create it!
                    # We want one instance with no params.
                    instanceParams=[{}]
                else:
                    continue
            if isinstance(instanceParams,dict):
                instanceParams=[instanceParams]
            instanceParams=typing.cast(InstanceParamsType,instanceParams)
            for instanceParamDict in instanceParams:
                if printObjectInstanciation:
                    paramsList=', '.join([f'{k}={repr(v)}' for k,v in instanceParamDict.items()])
                    print(f"CREATE PLUGIN: {pluginClass.__name__}({paramsList})")
                yield pluginClass(**instanceParamDict)
        except Exception:
            import traceback
            errStr=traceback.format_exc()
            print(f'Unable to create plugin {pluginInfo.name} due to error:\n{errStr}')


# -------------- Main entry point
def main(argv:typing.Iterable[str])->int:
    """
    Run the command line

    :param argv: command line arguments
    """
    if not isinstance(argv,list):
        argv=list(argv)
    printHelp=False
    didSomething=False
    for arg in argv[1:]:
        if arg.startswith('-'):
            kv=arg.split('=',1)
            k=kv[0].lower()
            if k=='--help':
                printHelp=True
            elif k in ('--ls','ls','-ls'):
                for plugin in findPlugins(None):
                    print(plugin)
                didSomething=True
            else:
                print(f'Unknown parameter "{k}"')
                printHelp=True
        else:
            print(f'Unknown parameter "{arg}"')
            printHelp=True
    if printHelp or not didSomething:
        print('This program will test access to plugins')
        print('USAGE:')
        print(f'  {argv[0]} [params]')
        print('PARAMS:')
        print('  --help ......... this help')
        print('  --ls ........... list all plugins')
        return -1
    return 0


if __name__=='__main__':
    import sys
    sys.exit(main(sys.argv))
