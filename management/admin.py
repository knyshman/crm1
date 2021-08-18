from django.contrib import admin
from .models import User, Interaction, Keyword
from django.contrib.auth.admin import UserAdmin


admin.site.register(User, UserAdmin)
admin.site.register(Interaction)
admin.site.register(Keyword)

