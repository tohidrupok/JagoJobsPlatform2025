from django.urls import path
from . import views

urlpatterns = [
    path('resume/', views.my_resume, name='view_resume'),
    path('resume/<int:resume_id>/', views.resume_detail, name='resume_detail'),
]