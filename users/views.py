from django.shortcuts import render
import random
import secrets

# from django.core.mail import send_mail
# from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView

# from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, PasswordRecoveryForm
from users.models import User
# from django.http import HttpResponseRedirect


class UserCreateView(CreateView):
    model = User
    template_name = 'users_app/user_form.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')  #('users:register_message')
