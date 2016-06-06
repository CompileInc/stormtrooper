from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model
    """

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'