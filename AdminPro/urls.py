from django.urls import path
from .views import superuser_dashboard, delete_profile

urlpatterns = [
    path('dashboard/', superuser_dashboard, name='superuser_dashboard'),
    path('delete-profile/<int:user_id>/', delete_profile, name='delete_profile'),
    
]
