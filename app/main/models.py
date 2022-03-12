import os
import cv2
import numpy as np
from django.core.mail import send_mail
from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile


class Gender(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'


class Client(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    gender = models.ForeignKey(Gender, models.CASCADE, blank=True, default=1)

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    @classmethod
    def create(cls, **kwargs):
        # Refactor fields
        kwargs['gender_id'] = kwargs['gender']
        kwargs.pop('gender')
        # Create Client
        client = cls(**kwargs)
        client.save()
        return client

    def save_avatar(self, image: np.array):
        image_name = self.avatar.name
        _format = image_name.split('.')[-1]
        _, image_bytes = cv2.imencode(f'.{_format}', image)
        self.avatar.save(image_name, ContentFile(image_bytes))
        return image_name

    def send_email_about_matching(self, matched_client):
        subject = f'Test Apptrix'
        text = f'Вы понравились {matched_client}! Почта участника: {matched_client.email}'
        return send_mail(subject, text, settings.DEFAULT_FROM_EMAIL, [f'{self.email}'],)

class Match(models.Model):
    from_client = models.ForeignKey(Client, models.CASCADE, related_name='match_from_client')
    to_client = models.ForeignKey(Client, models.CASCADE, related_name='match_to_client')
    date_time = models.DateTimeField(auto_now_add=True)
