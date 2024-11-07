import random

from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
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
        mailing_active_count = Mailing.objects.exclude(status="done").count()
        client_unique = Client.objects.all().distinct().count()
        blog_list = list(Blog.objects.all())
        random.shuffle(blog_list)

        context_data["mailing_count"] = mailing_count
        context_data["mailing_active_count"] = mailing_active_count
        context_data["client_unique"] = client_unique
        context_data["blog_list"] = blog_list[:3]

        return context_data


class MailingsListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailings_app/mailings_list.html"


class MailingsDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Mailing
    template_name = "mailings_app/mailings_detail.html"

    def test_func(self):
        mailing = self.get_object()
        return mailing.owner == self.request.user


class MailingsCreateView(LoginRequiredMixin, CreateView):
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


class MailingsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    template_name = "mailings_app/mailings_form.html"
    form_class = MailingForm
    success_url = reverse_lazy("mailings:mailings_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # if not self.request.user.is_superuser:
        kwargs.update({'request': self.request})
        return kwargs

    def test_func(self):
        mailing = self.get_object()
        return mailing.owner == self.request.user


class MailingsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    template_name = "mailings_app/mailings_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailings_list")

    def test_func(self):
        mailing = self.get_object()
        return mailing.owner == self.request.user


class MailingsChangeStatusView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    template_name = "mailings_app/mailings_change_status.html"
    form_class = MailingChangeStatusForm
    success_url = reverse_lazy("mailings:mailings_list")
    permission_required = ("mailings.can_change_status",)



class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "mailings_app/client_list.html"


class ClientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Client
    template_name = "mailings_app/client_detail.html"

    def test_func(self):
        mailing = self.get_object()
        return mailing.owner == self.request.user


class ClientCreateView(LoginRequiredMixin, CreateView):
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


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    template_name = "mailings_app/client_form.html"
    form_class = ClientForm
    success_url = reverse_lazy("mailings:client_list")

    def test_func(self):
        mailing = self.get_object()
        return mailing.owner == self.request.user


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    template_name = "mailings_app/client_confirm_delete.html"
    success_url = reverse_lazy("mailings:client_list")

    def test_func(self):
        mailing = self.get_object()
        return mailing.owner == self.request.user


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailings_app/message_list.html"


class MessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Message
    template_name = "mailings_app/message_detail.html"

    def test_func(self):
        mailing = self.get_object()
        return mailing.owner == self.request.user


class MessageCreateView(LoginRequiredMixin, CreateView):
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


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    template_name = "mailings_app/message_form.html"
    form_class = MessageForm
    success_url = reverse_lazy("mailings:message_list")

    def test_func(self):
        mailing = self.get_object()
        return mailing.owner == self.request.user


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    template_name = "mailings_app/message_confirm_delete.html"
    success_url = reverse_lazy("mailings:message_list")

    def test_func(self):
        mailing = self.get_object()
        return mailing.owner == self.request.user


class LogsListView(LoginRequiredMixin, ListView):
    model = Log
    template_name = "mailings_app/logs_list.html"

@login_required
def logs_delete(request):
    """ Удаление логов """
    logs = Log.objects.all()
    logs.delete()
    return HttpResponseRedirect('/mailings_list/')