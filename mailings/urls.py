from django.views.decorators.cache import cache_page
from django.urls import path

from mailings.apps import MailingsConfig
from mailings.views import StartPageView, MailingsListView, MailingsDetailView, MailingsCreateView, MailingsUpdateView, \
    MailingsDeleteView

app_name = MailingsConfig.name


urlpatterns = [
    path('', StartPageView.as_view(), name='start_page'),

    path('mailings_list/', MailingsListView.as_view(), name='mailings_list'),
    path('mailings_detail/<int:pk>/', MailingsDetailView.as_view(), name='mailings_detail'),
    path('mailings_create/', MailingsCreateView.as_view(), name='mailings_create'),
    path('mailings_update/<int:pk>/', MailingsUpdateView.as_view(), name='mailings_update'),
    path('mailings_delete/<int:pk>/', MailingsDeleteView.as_view(), name='mailings_delete'),

]

