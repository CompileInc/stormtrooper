from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from login.models import Trooper

admin.site.register(Trooper, UserAdmin)
