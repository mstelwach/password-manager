from django.conf.urls import url

from entry.autocomplete import EntrySiteNameAutocomplete, EntryLoginAutocomplete
from entry.views import *

app_name = 'entry'

urlpatterns = [
    url(r'^list/$', EntryListView.as_view(), name='list'),
    url(r'^create/$', EntryCreateView.as_view(), name='create'),
    url(r'^(?P<pk>[\d]+)/detail/$', EntryDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[\d]+)/update/$', EntryUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>[\d]+)/delete/$', EntryDeleteView.as_view(), name='delete'),
    url(r'^(?P<pk>[\d]+)/send-password/$', SendPasswordView.as_view(), name='send-password'),
    url(r'^link/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordActiveLink.as_view(), name='activate'),
    url(r'^export-to-csv/$', ExportToCsvView.as_view(), name='export-to-csv')
]

autocomplete_url_patterns = [
    url(r'^entry-site-name/autocomplete/$', EntrySiteNameAutocomplete.as_view(), name='site-name-autocomplete'),
    url(r'^entry-login/autocomplete/$', EntryLoginAutocomplete.as_view(), name='login-autocomplete'),
]

urlpatterns += autocomplete_url_patterns
