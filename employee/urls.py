from django.urls import path
from . import views

urlpatterns = [
    
    path('profile/', views.view_employer_profile, name='employer_profile'), 
    
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('core/profile/edit/', views.employer_profile, name='employer_profile_edit'),
    
]



