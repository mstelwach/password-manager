from django.db import models
from account.models import Account


class Entry(models.Model):
    site_name = models.CharField(max_length=128, null=False, blank=False)
    site_url = models.CharField(max_length=128, null=False, blank=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    login = models.CharField(max_length=64, blank=False, null=False)
    password = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Account: {}  | Login: {} | URL: {}'.format(self.account.username,
                                                           self.login,
                                                           self.site_url)
