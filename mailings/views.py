from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy

# Create your views here.

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from mailings.forms import MailingForm, MessageForm, ClientForm
from mailings.models import Mailing, Message, Client


class StartPageView(TemplateView):
    template_name = 'mailings_app/index.html'


class MailingsListView(ListView):
    model = Mailing
    template_name = 'mailings_app/mailings_list.html'


class MailingsDetailView(DetailView):
    model = Mailing
    template_name = 'mailings_app/mailings_detail.html'


class MailingsCreateView(CreateView):
    model = Mailing
    template_name = 'mailings_app/mailings_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailings_list')


class MailingsUpdateView(UpdateView):
    model = Mailing
    template_name = 'mailings_app/mailings_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailings_list')


class MailingsDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailings_app/mailings_confirm_delete.html'
    success_url = reverse_lazy('mailings:mailings_list')


class ClientListView(ListView):
    model = Client
    template_name = 'mailings_app/client_list.html'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailings_app/client_detail.html'


class ClientCreateView(CreateView):
    model = Client
    template_name = 'mailings_app/client_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('mailings_app:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'mailings_app/client_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('mailings_app:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailings_app/client_confirm_delete.html'
    success_url = reverse_lazy('mailings_app:client_list')
