from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ("1", 'student'),
        ("2", 'teacher'),
        ("3", 'supervisor'),
    )
    user_type = models.CharField(choices=USER_TYPE_CHOICES,default="1",null=False , max_length=10)

    def __str__(self):
        return self.username