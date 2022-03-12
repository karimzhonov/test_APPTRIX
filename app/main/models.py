import numpy as np
from django.core.mail import send_mail
from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile


class Gender(models.Model):
    """Пол"""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'


class Client(AbstractUser):
    """Участник"""
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    gender = models.ForeignKey(Gender, models.CASCADE, blank=True)
    longitude = models.FloatField(blank=True, default=0)
    latitude = models.FloatField(blank=True, default=0)

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def save_avatar(self, image: np.array) -> str:
        """
        Сохранение изображения
        :param image: np.array
        :return: image_name
        """
        import cv2.cv2 as cv2

        image_name = self.avatar.name
        _format = image_name.split('.')[-1]
        _, image_bytes = cv2.imencode(f'.{_format}', image)
        self.avatar.save(image_name, ContentFile(image_bytes))
        return image_name

    def send_email_about_matching(self, matched_client) -> int:
        """
        Отправления писмо на почты
        :param matched_client: Client model
        :return: status (1 or 0)
        """
        subject = f'Test Apptrix'
        text = f'Вы понравились {matched_client}! Почта участника: {matched_client.email}'
        return send_mail(subject, text, settings.DEFAULT_FROM_EMAIL, [f'{self.email}'], )

    def get_position(self):
        pass

    def get_distance(self, latitude_longitude: tuple[int, int]) -> float:
        """
        Рассчитать расстояние
        :param latitude_longitude: tuple[широта, долгота]
        :return: расстояние
        """
        latitude, longitude = latitude_longitude
        l = 111100
        return np.arccos(np.sin(self.latitude)*np.sin(latitude) + np.cos(self.latitude)*np.cos(latitude)*np.cos(longitude - self.longitude))*l

    def get_distance_str(self, l = 111100) -> str:
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

    def __str__(self):
        return f'From: {self.from_client} To: {self.to_client}'

    class Meta:
        verbose_name = 'Симпатия'
        verbose_name_plural = 'Симпатий'
        ordering = ['-date_time']