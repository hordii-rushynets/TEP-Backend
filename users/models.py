from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    police = models.BooleanField(default=False)
    wantInfo = models.BooleanField(default=False)
    wholesale = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
