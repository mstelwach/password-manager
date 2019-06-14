import django_tables2 as tables

from entry.models import Entry


class EntryTable(tables.Table):
    actions = tables.TemplateColumn(template_name='entry/table_actions.html', verbose_name="Actions",
                                    orderable=False)
    hide_password = tables.Column(default='******', verbose_name='Password', orderable=False)

    class Meta:
        model = Entry
        template = 'tables2_bootstrap4.html'
        fields = ['site_name', 'site_url', 'login', 'hide_password', 'date', 'actions']

