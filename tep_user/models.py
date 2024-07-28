"""Model for tep_user app."""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from tep_user.constants import USER_EMAIL_REQUIRED


class TEPUserManager(BaseUserManager):
    """Override the behavior of the create_user and create_superuser methods."""
    def create_user(self, email: str, password: str = None, **extra_fields) -> AbstractUser:
        """
        Create user using email as required field.

        :param email: user email.
        :param password: user email.
        :param extra_fields: other fields of User model.

        :raises ValueError: email is not set.

        :return: user instance.
        """
        if not email:
            raise ValueError(USER_EMAIL_REQUIRED)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create superuser using email as required field.

        :param email: user email.
        :param password: user email.
        :param extra_fields: other fields of User model.

        :return: user instance.
        """
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        extra_fields['username'] = email
        return self.create_user(email, password, **extra_fields)


class TEPUser(AbstractUser):
    """User model."""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    privacy_policy_accepted = models.BooleanField(default=False)
    subscribed_to_updates = models.BooleanField(default=False)
    interested_in_wholesale = models.BooleanField(default=False)
    username = models.CharField(max_length=150, default='default_username')
    birth_date = models.DateField(null=True, blank=True)

    address = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    region = models.CharField(max_length=128, null=True, blank=True)
    index = models.PositiveIntegerField(null=True, blank=True)

    phone_communication = models.BooleanField(default=False)
    email_communication = models.BooleanField(default=True)

    objects = TEPUserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()


class TEPUserSocialNetworks(models.Model):
    """User social networks model."""
    SOCIAL_NETWORK_TYPES = (
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('youtube', 'YouTube'),
        ('pinterest', 'Pinterest'),
        ('linkedin', 'LinkedIn')
    )

    types = models.CharField(max_length=50, choices=SOCIAL_NETWORK_TYPES, default=SOCIAL_NETWORK_TYPES[0][0])
    url = models.URLField(default='#')
    user = models.ForeignKey(TEPUser, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.user.email} - {self.types}'
