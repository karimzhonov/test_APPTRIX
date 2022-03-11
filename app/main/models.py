import os
import cv2
import numpy as np
from django.db import models
from django.conf import settings
from datetime import datetime
import hashlib


class Gender(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'


class Client(models.Model):
    avatar = models.ImageField(upload_to='avatars/')
    gender = models.ForeignKey(Gender, models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.SlugField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    @staticmethod
    def hashing_sha256(text):
        return hashlib.sha256(text.encode()).hexdigest()

    @classmethod
    def auth(cls, username, password):
        try:
            client = cls.objects.get(username=username)
        except cls.objects.model.DoesNotExist:
            return False, None
        else:
            if client.password == cls.hashing_sha256(password):
                return True, client
            else:
                return False, None

    @classmethod
    def create(cls, **kwargs):
        # Refactor fields
        kwargs['password'] = cls.hashing_sha256(kwargs['password'])
        kwargs['gender_id'] = kwargs['gender']
        kwargs.pop('gender')
        # Create Client
        client = cls(**kwargs)
        client.avatar = cls.avatar.field.generate_filename(client.avatar.instance, kwargs['avatar'])
        client.save()
        return client

    def save_avatar(self, image: np.array):
        image_name = self.avatar.name
        if os.path.exists(image_name):
            dtime = datetime.now()
            new_name_list = image_name.split('.')
            new_name_list[-2] += f'{dtime}'
            self.avatar = '.'.join(new_name_list)
            return self.save_avatar(image)
        cv2.imwrite(os.path.join(settings.MEDIA_ROOT, image_name), image)
        return image_name
