from __future__ import unicode_literals
import hashlib
import urllib

from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Trooper(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def profile_pic(self):
        email_hash = hashlib.md5(self.email.lower()).hexdigest()
        keys = {'d': settings.DEFAULT_AVATAR,
                'size': 30,
                }
        keys = urllib.urlencode(keys)
        return "https://www.gravatar.com/avatar/{hash}?{query}".format(hash=email_hash,
                                                                       query=keys)
