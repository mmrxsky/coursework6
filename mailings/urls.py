from django.views.decorators.cache import cache_page
from django.urls import path

from mailings.apps import MailingsConfig
from mailings.views import (
    StartPageView,
    MailingsListView,
    MailingsDetailView,
    MailingsCreateView,
    MailingsUpdateView,
    MailingsDeleteView,
    ClientListView,
    ClientDetailView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    MessageListView,
    MessageDetailView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    LogsListView,
)

app_name = MailingsConfig.name


urlpatterns = [
    path("", StartPageView.as_view(), name="start_page"),
    path("mailings_list/", MailingsListView.as_view(), name="mailings_list"),
    path(
        "mailings_detail/<int:pk>/",
        MailingsDetailView.as_view(),
        name="mailings_detail",
    ),
    path("mailings_create/", MailingsCreateView.as_view(), name="mailings_create"),
    path(
        "mailings_update/<int:pk>/",
        MailingsUpdateView.as_view(),
        name="mailings_update",
    ),
    path(
        "mailings_delete/<int:pk>/",
        MailingsDeleteView.as_view(),
        name="mailings_delete",
    ),
    path("client_list/", ClientListView.as_view(), name="client_list"),
    path("client_detail/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("client_create/", ClientCreateView.as_view(), name="client_create"),
    path("client_update/<int:pk>/", ClientUpdateView.as_view(), name="client_update"),
    path("client_delete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),
    path("message_list/", MessageListView.as_view(), name="message_list"),
    path(
        "message_detail/<int:pk>/", MessageDetailView.as_view(), name="message_detail"
    ),
    path("message_create/", MessageCreateView.as_view(), name="message_create"),
    path(
        "message_update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "message_delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path("logs_list/", LogsListView.as_view(), name="logs_list"),
]
