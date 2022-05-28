from django.contrib import admin
from .models import MyUser, SocialLink

admin.site.register(MyUser)
admin.site.register(SocialLink)

