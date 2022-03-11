from rest_framework import serializers
from .models import Client

class CreateClientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Client