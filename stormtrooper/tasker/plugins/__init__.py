class Plugin(object):
    @classmethod
    def process(self, answers):
        '''Implement your answer normalization/manipulation here'''
        return answers


def all_subclasses(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__()
                                   for g in all_subclasses(s)]

ALL_PLUGINS = []
ALL_PLUGIN_CHOICES = []
ALL_PLUGIN_MAP = {}


def discover_and_import_plugins():
    import os
    current_directory = os.path.dirname(os.path.realpath(__file__))
    for fn in os.listdir(current_directory):
        if fn.endswith("_plugin.py"):
            f = "%s/%s" % (current_directory, fn)
            execfile(f)


def initialize_plugins():
    discover_and_import_plugins()

    global ALL_PLUGINS
    global ALL_PLUGIN_CHOICES
    global ALL_PLUGIN_MAP

    ALL_PLUGINS = all_subclasses(Plugin)
    if len(set([p.plugin_name for p in ALL_PLUGINS])) != len(ALL_PLUGINS):
        raise Exception("Possible plugin name collision.")

    for plugin in ALL_PLUGINS:
        ALL_PLUGIN_MAP[plugin.plugin_name] = plugin
        ALL_PLUGIN_CHOICES.append([plugin.plugin_name, plugin.plugin_name_verbose])


def get_plugin(plugin_name):
    global ALL_PLUGIN_MAP
    return ALL_PLUGIN_MAP[plugin_name]
