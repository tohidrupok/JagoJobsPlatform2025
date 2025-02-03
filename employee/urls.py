from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    
]



