from rest_framework import serializers
from .models import Client


class CreateClientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['avatar', 'username', 'password', 'first_name', 'last_name', 'email', 'gender']
        model = Client


class AuthClientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['username', 'password']
        model = Client

class ShowClientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['avatar', 'username', 'first_name', 'last_name', 'email', 'gender']
        model = Client