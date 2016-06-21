from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser


class Trooper(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
