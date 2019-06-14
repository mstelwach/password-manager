from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import validate_email
from django.db import models
from django.utils import timezone


class Account(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    username = models.CharField(max_length=32,
                                unique=True,
                                help_text='Required. 32 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                validators=[username_validator],
                                error_messages={
                                    'unique': "A user with that username already exists.",
                                }, )
    email = models.EmailField(
        unique=True,
        validators=[validate_email],
        error_messages={
            'unique': "A user with that email address already exists."
        }
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['email']

    def __str__(self):
        return 'Account: {}'.format(self.username)
