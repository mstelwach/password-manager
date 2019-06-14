from django.contrib import admin

from entry.models import Entry


class EntryAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'site_url', 'account', 'login', 'password']


admin.site.register(Entry, EntryAdmin)