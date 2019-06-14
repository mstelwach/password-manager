from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin

from entry.models import Entry


class EntrySiteNameAutocomplete(LoginRequiredMixin, autocomplete.Select2ListView):
    """
    Site name field autocomplete
    """

    def get_list(self):
        queryset = Entry.objects.filter(account=self.request.user)
        queryset = list(queryset.values_list('site_name', flat=True))
        queryset.append(self.q)
        return queryset


class EntryLoginAutocomplete(LoginRequiredMixin, autocomplete.Select2ListView):
    """
    Login field autocomplete
    """

    def get_list(self):
        queryset = Entry.objects.filter(account=self.request.user)
        queryset = list(queryset.values_list('login', flat=True))
        queryset.append(self.q)
        return queryset

