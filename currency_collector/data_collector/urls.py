from django.urls import path

from django.urls import path
from . import views

urlpatterns = [
    path('show_rates/', views.show_rates, name='show_rates'),
    path('fetch_currency_data/', views.fetch_currency, name='fetch_currency_data'),
]
