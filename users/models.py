from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    policy = models.BooleanField(default=False)
    wantInfo = models.BooleanField(default=False)
    wholesale = models.BooleanField(default=False)
    username = models.CharField(max_length=150, default='default_username')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'first_name', 'policy', 'wantInfo', 'wholesale']

    def __str__(self):
        return self.email
