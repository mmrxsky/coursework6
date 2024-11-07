from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
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

from mailings.forms import MailingForm, MessageForm, ClientForm, MailingChangeStatusForm
from mailings.models import Mailing, Message, Client, Log
from blog.models import Blog


class StartPageView(TemplateView):
    template_name = "mailings_app/index.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        mailing_count = Mailing.objects.all().count()
        mailing_active_count = Mailing.objects.exclude(status = "done").count()
        client_unique = Client.objects.all().distinct().count()
        blog_random = Blog.objects.order_by('?')[:3]
        blog_1 = blog_random[0]
        blog_2 = blog_random[1]
        blog_3 = blog_random[2]

        context_data["mailing_count"] = mailing_count
        context_data["mailing_active_count"] = mailing_active_count
        context_data["client_unique"] = client_unique
        context_data["blog_1"] = blog_1
        context_data["blog_2"] = blog_2
        context_data["blog_3"] = blog_3

        return context_data


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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # if not self.request.user.is_superuser:
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        """Добавление владельца рассылке"""
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # if not self.request.user.is_superuser:
        kwargs.update({'request': self.request})
        return kwargs


class MailingsDeleteView(DeleteView):
    model = Mailing
    template_name = "mailings_app/mailings_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailings_list")


class MailingsChangeStatusView(UpdateView):
    model = Mailing
    template_name = "mailings_app/mailings_change_status.html"
    form_class = MailingChangeStatusForm
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
        """Добавление владельца клиенту"""
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
        """Добавление владельца сообщению"""
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


def logs_delete(request):
    """ Удаление логов """
    logs = Log.objects.all()
    logs.delete()
    return HttpResponseRedirect('/mailings_list/')
