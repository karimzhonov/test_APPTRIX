from rest_framework import serializers
from .models import Client


class CreateClientSerializer(serializers.ModelSerializer):
    """Serializers для создание участника"""
    class Meta:
        fields = ['avatar', 'username', 'password', 'first_name', 'last_name', 'email', 'gender']
        model = Client


class AuthClientSerializer(serializers.ModelSerializer):
    """Serializers для авторизация участника"""
    class Meta:
        fields = ['username', 'password']
        model = Client


class ShowClientSerializer(serializers.ModelSerializer):
    """Serializers для показа участника(без пароля)"""
    class Meta:
        fields = ['avatar', 'username', 'first_name', 'last_name', 'email', 'gender', 'latitude', 'longitude', 'id']
        model = Client


class CoordinateClientSerializer(serializers.Serializer):
    """Serializers для коррекция координат участника"""
    longitude = serializers.IntegerField()
    latitude = serializers.IntegerField()
