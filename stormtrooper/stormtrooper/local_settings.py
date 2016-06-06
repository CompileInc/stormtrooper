from stormtrooper.settings import BASE_DIR

MEDIA_ROOT = "%s/media/" % (BASE_DIR)
STATIC_ROOT = "%s/static/" % (BASE_DIR)

MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'login.CustomUser'
