from django.db import models

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

    