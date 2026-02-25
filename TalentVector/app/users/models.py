from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=50)
    username = models.CharField(max_length=30, unique=True)
    USERNAME_FIELD = 'email'

    # Solamente sirve para establecer que campos son requeridos el crear un usario desde la consola con el comando:
    # python manage.py createsuperuser
    # REQUIRED_FIELDS = ['username', 'name', 'surname']

    def __str__(self):
        return f'{self.name}, {self.surname}, {self.email}'
    