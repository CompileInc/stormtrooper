from stormtrooper.settings import BASE_DIR, INSTALLED_APPS, PROJECT_DIR, SETTINGS_EXPORT

INSTALLED_APPS = INSTALLED_APPS + ('django_seed', )

MEDIA_ROOT = "%s/media/" % (BASE_DIR)
STATIC_ROOT = "%s/static/" % (BASE_DIR)

MEDIA_URL = '/media/'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '326290971528-4174mkl76s9rpm5260cs5qb4jfjjtfom.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'iIzzqq7MCZ7WAayzagO2ekyy'

SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ['compile.com']
SETTINGS_EXPORT = SETTINGS_EXPORT + ['SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS']

SENTRY_ENABLE = False

if SENTRY_ENABLE:
    import raven
    RAVEN_CONFIG = {
        'dsn': '<YOUR_DSN_HERE>',
        'release': raven.fetch_git_sha(PROJECT_DIR)
    }
    INSTALLED_APPS = INSTALLED_APPS + ('raven.contrib.django.raven_compat', )
    SETTINGS_EXPORT = SETTINGS_EXPORT + ['RAVEN_CONFIG']
