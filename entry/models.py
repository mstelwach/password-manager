from django.core.validators import URLValidator
from django.db import models
from django.utils.crypto import get_random_string

from account.models import Account


class OptionalSchemeURLValidator(URLValidator):
    def __call__(self, value):
        if '://' not in value:
            value = 'http://' + value
        super(OptionalSchemeURLValidator, self).__call__(value)


class Entry(models.Model):
    site_name = models.CharField(max_length=128)
    site_url = models.CharField(max_length=256, validators=[OptionalSchemeURLValidator()])
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    login = models.CharField(max_length=64)
    password = models.CharField(max_length=64, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Account: {}  | Login: {} | URL: {}'.format(self.account.username,
                                                           self.login,
                                                           self.site_url)

    @staticmethod
    def make_random_password(length=16, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
        return get_random_string(length, allowed_chars)

