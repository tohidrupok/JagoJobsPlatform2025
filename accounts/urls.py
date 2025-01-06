from django.urls import path
from . import views

urlpatterns = [
    path('register/seeker/', views.register_seeker, name='register_seeker'),
    path('register/employer/', views.register_employer, name='register_employer'),
    
    
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('dashboard/seeker/', views.seeker_dashboard, name='seeker_dashboard'),
    path('dashboard/employer/', views.employer_dashboard, name='employer_dashboard'),
    
    # Manager Registration
    path('register/manager/', views.register_manager, name='register_manager'),
    path('dashboard/manager/', views.manager_dashboard, name='manager_dashboard'),
    path('employee/approve-managers/', views.approve_manager_list, name='approve_manager_list'),
    path('employee/approve-managers/<int:user_id>/', views.approve_manager, name='approve_manager'),
    
]
