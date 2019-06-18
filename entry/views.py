import csv
from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView, RedirectView
from django_tables2 import RequestConfig

from entry.admin import EntryAdmin
from entry.filters import EntryListFilter
from entry.forms import EntryCreateForm, EntryUpdateForm, SendPasswordForm
from entry.models import Entry
from entry.tables import EntryTable
from entry.tokens import password_activation_token, PasswordCrypto


class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = "entry/list.html"
    table_class = EntryTable
    paginate_by = 10

    def get_queryset(self):
        return Entry.objects.filter(account=self.request.user)

    def filter_data(self, context):
        filtered_data = EntryListFilter(self.request.GET, queryset=self.get_queryset())
        context['filtered_data'] = filtered_data
        filtered_entry_table = self.table_class(filtered_data.qs)
        return filtered_entry_table

    def get_context_data(self, **kwargs):
        context = super(EntryListView, self).get_context_data(**kwargs)
        entry_table = self.filter_data(context)
        RequestConfig(self.request, paginate={'per_page': self.paginate_by}).configure(entry_table)
        context['entry_table'] = entry_table
        context['full_url'] = self.request.path
        return context


class EntryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Entry
    form_class = EntryCreateForm
    template_name = 'entry/create.html'
    success_message = "The password\'s record was created successfully."
    secret_key = force_bytes(settings.SECRET_KEY)

    def get_success_url(self):
        if self.request.POST.get('save'):
            return reverse_lazy('entry:list')
        else:
            return reverse_lazy('entry:create')

    def form_valid(self, form):
        form.instance.account = self.request.user
        crypto = PasswordCrypto(self.secret_key)
        if not form.cleaned_data['password']:
            form.instance.password = crypto.encrypt(self.model.make_random_password())
        else:
            form.instance.password = crypto.encrypt(form.cleaned_data['password'])
        return super(EntryCreateView, self).form_valid(form)


class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = 'entry/detail.html'
    secret_key = force_bytes(settings.SECRET_KEY)

    def get_context_data(self, **kwargs):
        entry = self.get_object()
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        crypto = PasswordCrypto(self.secret_key)
        p = entry.password.lstrip("b'")
        decrypt_password = crypto.decrypt(force_bytes(p))
        context['decrypt_password'] = decrypt_password
        context['hide_password'] = '******'
        return context


class EntryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Entry
    form_class = EntryUpdateForm
    template_name = "entry/update.html"
    success_url = reverse_lazy('entry:list')
    success_message = "The password\'s record was updated successfully."
    secret_key = force_bytes(settings.SECRET_KEY)

    def form_valid(self, form):
        entry = self.get_object()
        crypto = PasswordCrypto(self.secret_key)
        if not form.cleaned_data['password']:
            form.instance.password = entry.password
        else:
            form.instance.password = crypto.encrypt(form.cleaned_data['password'])
        return super(EntryUpdateView, self).form_valid(form)


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    success_url = reverse_lazy('entry:list')
    success_message = "The password\'s record was deleted successfully."

    def delete(self, request, *args, **kwargs):
        delete = super(EntryDeleteView, self).delete(request, *args, **kwargs)
        return delete


class SendPasswordView(LoginRequiredMixin, FormView):
    form_class = SendPasswordForm
    template_name = 'entry/send_password.html'
    success_message = "Email with password was sent successfully."
    success_url = reverse_lazy('entry:list')
    email_subject = '{} has sent data login'

    def get_form_kwargs(self):
        kwargs = super(SendPasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def send_message(self):
        entry = get_object_or_404(Entry, pk=self.kwargs.get('pk'))
        message = render_to_string('entry/email.html', {
            'sender': self.request.user,
            'receiver': self.receiver,
            'entry': entry,
            'uid': urlsafe_base64_encode(force_bytes(entry.pk)),
            'token': password_activation_token.make_token(entry),
        })

        email_subject = self.email_subject.format(self.request.user.username)
        email = EmailMultiAlternatives(email_subject, to=[self.receiver.email])
        email.attach_alternative(message, 'text/html')

        try:
            email.send()
        except SMTPException as e:
            messages.error("Email had not been sent. There was the problem with {}".format(e))

    def form_valid(self, form):
        self.receiver = form.cleaned_data['receiver']
        self.send_message()
        return super(SendPasswordView, self).form_valid(form)


class PasswordActiveLink(DetailView):
    model = Entry
    template_name = 'entry/password_active_link.html'
    secret_key = force_bytes(settings.SECRET_KEY)

    def dispatch(self, request, *args, **kwargs):
        try:
            uidb64 = self.kwargs.get('uidb64')
            uid = force_text(urlsafe_base64_decode(uidb64))
            self.entry = Entry.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Entry.DoesNotExist):
            self.entry = None
        token = self.kwargs.get('token')
        if self.entry is not None and password_activation_token.check_token(self.entry, token):
            return super(PasswordActiveLink, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponse('Activation link is invalid!')

    def get_object(self, queryset=None):
        object = self.entry
        return object

    def get_context_data(self, **kwargs):
        context = super(PasswordActiveLink, self).get_context_data(**kwargs)
        entry = self.get_object()
        crypto = PasswordCrypto(self.secret_key)
        p = entry.password.lstrip("b'")
        decrypt_password = crypto.decrypt(force_bytes(p))
        context['decrypt_password'] = decrypt_password
        return context


class ExportToCsvView(LoginRequiredMixin, View):

    def download_csv(self, modeladmin, request, queryset):
        opts = queryset.model._meta
        response = HttpResponse(content_type='text/csv')
        writer = csv.writer(response)
        field_names = [field.name for field in opts.fields]
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response

    def get(self, request):
        data = self.download_csv(EntryAdmin, request, Entry.objects.filter(account=self.request.user))
        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}-entries.csv"'.format(self.request.user.username)
        return response