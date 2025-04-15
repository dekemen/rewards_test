from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    coins = models.IntegerField(default=0)

    def add_coins(self, amount):
        if amount < 0:
            raise ValueError("Количество монет не может быть меньше 0")
        self.coins += amount
        self.save()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
