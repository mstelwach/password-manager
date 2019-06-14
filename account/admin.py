from django.contrib import admin

from account.models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'password']


admin.site.register(Account, AccountAdmin)

