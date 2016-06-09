from stormtrooper.settings import BASE_DIR

MEDIA_ROOT = "%s/media/" % (BASE_DIR)
STATIC_ROOT = "%s/static/" % (BASE_DIR)

MEDIA_URL = '/media/'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '326290971528-4174mkl76s9rpm5260cs5qb4jfjjtfom.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'iIzzqq7MCZ7WAayzagO2ekyy'

SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ['compile.com']