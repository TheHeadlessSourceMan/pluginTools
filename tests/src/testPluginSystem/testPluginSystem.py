import typing
from pluginSystem import createPlugins
from pluginTools import findPlugins

PLUGIN_TYPE='testPluginSystem.person_plugin'


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
                print("Registered plugins:")
                for plugin in findPlugins(PLUGIN_TYPE):
                    print(plugin)
                didSomething=True
            elif k in ('--create'):
                plugins=list(createPlugins(PLUGIN_TYPE))
                print("Created plugins:")
                for plugin in plugins:
                    print(type(plugin))
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
        print('  --create ....... create instances of all plugins')
        return -1
    return 0


if __name__=='__main__':
    import sys
    sys.exit(main(sys.argv))
