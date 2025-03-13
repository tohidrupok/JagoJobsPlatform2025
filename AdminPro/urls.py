from django.urls import path
from .views import superuser_dashboard

urlpatterns = [
    path('dashboard/', superuser_dashboard, name='superuser_dashboard'),
]
