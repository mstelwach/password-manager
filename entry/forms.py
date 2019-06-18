from django import forms

from account.models import Account
from entry.models import Entry


class EntryCreateForm(forms.ModelForm):

    class Meta:
        model = Entry
        exclude = ['account', 'date']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Leave blank to generate one'})
        }


class EntryUpdateForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ['site_name', 'site_url', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class SendPasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SendPasswordForm, self).__init__(*args, **kwargs)
        self.fields['receiver'] = forms.ModelChoiceField(queryset=Account.objects.exclude(username=user.username))
