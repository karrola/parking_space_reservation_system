from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.

# CustomUser model (logowanie za pomocą maila zamiast username)
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email