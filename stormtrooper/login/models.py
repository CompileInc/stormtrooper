from __future__ import unicode_literals
import hashlib

from django.contrib.auth.models import AbstractUser


class Trooper(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def profile_pic(self):
        email_hash = hashlib.md5(self.email.lower()).hexdigest()
        size = 30
        default = 'retro'
        return "https://www.gravatar.com/avatar/{hash}?d={default}&size={size}".format(hash=email_hash,
                                                                                       default=default,
                                                                                       size=size)
