from users.forms import LoginCustomForm
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, RegisterMessageView

app_name = UsersConfig.name


urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="users_app/login.html", form_class=LoginCustomForm
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("email_confirm/<str:code>/", email_verification, name="email_confirm"),
    # path('register/email_confirm/<str:token>/', email_verification, name='email_confirm'),
    path("register/message/", RegisterMessageView.as_view(), name="register_message"),
    # path('password_recovery/', PasswordRecoveryView.as_view(), name='password_recovery'),
    # # path('password_recovery/create_new_password/<str:code>', create_new_password, name='create_new_password'),
    # path('password_recovery/message/', PasswordRecoveryMessageView.as_view(), name='recovery_message')
]
