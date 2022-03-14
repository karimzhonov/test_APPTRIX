from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(Client, UserAdmin)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    class Meta:
        fields = "__all__"
