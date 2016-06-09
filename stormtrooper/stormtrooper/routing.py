from django.conf import settings
from django.utils.module_loading import import_module


def get_channel_routings():
    channel_routing = []
    for app in settings.INSTALLED_APPS:
        try:
            routing = import_module("{}.routing".format(app))
            channel_routing.extend(routing.channel_routing)
        except:
            continue
    return channel_routing

channel_routing = get_channel_routings()
