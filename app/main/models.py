import numpy as np
from django.core.mail import send_mail
from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile


class Client(AbstractUser):
    """Участник"""
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    gender = models.CharField(max_length=255, blank=True)
    longitude = models.FloatField(blank=True, default=0)
    latitude = models.FloatField(blank=True, default=0)

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def save_avatar(self, image) -> str:
        """
        Сохранение изображения
        :param image: bytes
        :return: image_name
        """

        image_name = self.avatar.name
        self.avatar.save(image_name, ContentFile(image))
        return image_name

    def send_email_about_matching(self, matched_client) -> int:
        """
        Отправления писмо на почты
        :param matched_client: Client model
        :return: status (1 or 0)
        """
        subject = f'Test Apptrix'
        text = f'Вы понравились {matched_client}! Почта участника: {matched_client.email}'
        return send_mail(subject, text, settings.DEFAULT_FROM_EMAIL, [f'{self.email}'], True)

    def get_distance(self, latitude_longitude: tuple[int, int], l: int = 111100) -> float:
        """
        Рассчитать расстояние
        :param latitude_longitude: tuple[широта, долгота]
        :param l: длина дуги 1° меридиана (на Земле l=111,1 км)
        :return: расстояние
        """
        latitude, longitude = latitude_longitude
        return np.arccos(np.sin(self.latitude) * np.sin(latitude) + np.cos(self.latitude) * np.cos(latitude) * np.cos(
            longitude - self.longitude)) * l

    def get_distance_str(self, l: int = 111100) -> str:
        """
        Формула Great-circle_distance для запроса sql
        :param l: длина дуги 1° меридиана (на Земле l=111,1 км)
        """
        f = f'ACOS(SIN({self.latitude})*SIN(latitude)+COS({self.latitude})*COS(latitude)*COS(longitude - {self.longitude}))'
        return f'{l}*{f}'


class Match(models.Model):
    """Симпатия"""
    from_client = models.ForeignKey(Client, models.CASCADE, related_name='match_from_client')
    to_client = models.ForeignKey(Client, models.CASCADE, related_name='match_to_client')
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'From: {self.from_client} To: {self.to_client}'

    class Meta:
        verbose_name = 'Симпатия'
        verbose_name_plural = 'Симпатий'
        ordering = ['-date_time']
