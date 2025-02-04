from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('profile/', views.employer_profile, name='employer_profile'),
    path('profile/edit', views.edit_employer_profile, name='employer_profile'),
    
]



