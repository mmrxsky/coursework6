from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from mailings.forms import MailingForm, MessageForm
from mailings.models import Mailing, Message


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

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(Mailing, Message, form=MessageForm, extra=1)

        if self.request.method == 'POST':
            formset = MessageFormset(self.request.POST, instance=self.object)
        else:
            formset = MessageFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data


class MailingsUpdateView(UpdateView):
    model = Mailing
    template_name = 'mailings_app/mailings_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailings_list')


class MailingsDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailings_app/mailings_confirm_delete.html'
    success_url = reverse_lazy('mailings:mailings_list')
