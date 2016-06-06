from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from login.models import CustomUser

admin.site.register(CustomUser, UserAdmin)
