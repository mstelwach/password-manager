import django_filters
from dal import autocomplete
from django_filters.widgets import RangeWidget
from entry.models import Entry


class MyRangeWidget(RangeWidget):
    '''
    Using for date range field
    '''
    def __init__(self, from_attrs=None, to_attrs=None, attrs=None):
        super(MyRangeWidget, self).__init__(attrs)

        if from_attrs:
            self.widgets[0].attrs.update(from_attrs)
        if to_attrs:
            self.widgets[1].attrs.update(to_attrs)


class EntryListFilter(django_filters.FilterSet):

    site_name = django_filters.ChoiceFilter(
        choices=Entry.objects.all().values_list('site_name', 'site_name'),
        widget=autocomplete.ListSelect2(
            url='entry:site-name-autocomplete',
            attrs={'data-placeholder': 'Site name', 'class': 'invisible'}
        )
    )

    login = django_filters.ChoiceFilter(
        choices=Entry.objects.all().values_list('login', 'login'),
        widget=autocomplete.ListSelect2(
            url='entry:login-autocomplete',
            attrs={'data-placeholder': 'Login', 'class': 'invisible'}
        )
    )
    date = django_filters.DateFromToRangeFilter(
        field_name='created__date',
        widget=MyRangeWidget(from_attrs={'placeholder': 'Start date'}, to_attrs={'placeholder': 'End date'}))

    class Meta:
        model = Entry
        fields = ['date']

