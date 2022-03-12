from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


admin.site.register(Client, UserAdmin)

@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    class Meta:
        fields = "__all__"