from django.shortcuts import render
import random
import secrets


from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView

from config import settings

from users.forms import UserRegisterForm, PasswordRecoveryForm
from users.models import User
from django.http import HttpResponseRedirect


class RegisterMessageView(TemplateView):
    template_name = 'users_app/register_message.html'


class UserCreateView(CreateView):
    model = User
    template_name = 'users_app/user_form.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:register_message')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        code = secrets.token_hex(8)
        user.code = code
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email_confirm/{code}/'

        send_mail(
            subject='Подтверждение почты',
            message=f'Перейдите по ссылке для подтверждения почты {url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)

def email_verification(request, code):
    user = get_object_or_404(User, code=code)
    user.is_active = True
    user.save()
    return HttpResponseRedirect('/users/login/')
