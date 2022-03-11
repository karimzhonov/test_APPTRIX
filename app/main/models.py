from django.db import models
import hashlib


# Create your models here.
class Gender(models.Model):
    name = models.CharField(max_length=255, unique=True)


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
    def _hashing_sha256(text: str):
        return hashlib.sha256(text).hexdigest()

    @classmethod
    def auth(cls, username, password):
        try:
            client = cls.objects.get(username=username)
        except cls.objects.model.DoesNotExist:
            return False, None
        else:
            if client.password == cls._hashing_sha256(password):
                return True, client
            else:
                return False, None

    @classmethod
    def create(cls, **kwargs):
        kwargs['password'] = cls._hashing_sha256(kwargs['password'])

        return cls.objects.create(**kwargs)
