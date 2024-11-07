from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from mailings.forms import MailingForm, MessageForm, ClientForm
from mailings.models import Mailing, Message, Client, Log


class StartPageView(TemplateView):
    template_name = "mailings_app/index.html"


class MailingsListView(ListView):
    model = Mailing
    template_name = "mailings_app/mailings_list.html"


class MailingsDetailView(DetailView):
    model = Mailing
    template_name = "mailings_app/mailings_detail.html"


class MailingsCreateView(CreateView):
    model = Mailing
    template_name = "mailings_app/mailings_form.html"
    form_class = MailingForm
    success_url = reverse_lazy("mailings:mailings_list")

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({'request': self.request})
    #     return kwargs

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     user = self.request.user
    #     return queryset.filter(user=user)

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingsUpdateView(UpdateView):
    model = Mailing
    template_name = "mailings_app/mailings_form.html"
    form_class = MailingForm
    success_url = reverse_lazy("mailings:mailings_list")


class MailingsDeleteView(DeleteView):
    model = Mailing
    template_name = "mailings_app/mailings_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailings_list")


class ClientListView(ListView):
    model = Client
    template_name = "mailings_app/client_list.html"


class ClientDetailView(DetailView):
    model = Client
    template_name = "mailings_app/client_detail.html"


class ClientCreateView(CreateView):
    model = Client
    template_name = "mailings_app/client_form.html"
    form_class = ClientForm
    success_url = reverse_lazy("mailings:client_list")

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    template_name = "mailings_app/client_form.html"
    form_class = ClientForm
    success_url = reverse_lazy("mailings:client_list")


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "mailings_app/client_confirm_delete.html"
    success_url = reverse_lazy("mailings:client_list")


class MessageListView(ListView):
    model = Message
    template_name = "mailings_app/message_list.html"


class MessageDetailView(DetailView):
    model = Message
    template_name = "mailings_app/message_detail.html"


class MessageCreateView(CreateView):
    model = Message
    template_name = "mailings_app/message_form.html"
    form_class = MessageForm
    success_url = reverse_lazy("mailings:message_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    template_name = "mailings_app/message_form.html"
    form_class = MessageForm
    success_url = reverse_lazy("mailings:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "mailings_app/message_confirm_delete.html"
    success_url = reverse_lazy("mailings:message_list")


class LogsListView(ListView):
    model = Log
    template_name = "mailings_app/logs_list.html"
