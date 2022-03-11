from django.contrib import admin
from .models import *

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    class Meta:
        fields = "__all__"


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    class Meta:
        fields = "__all__"