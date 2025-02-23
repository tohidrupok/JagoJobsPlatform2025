from django.urls import path
from .views import (
    job_list, job_detail, apply_job, employee_applications
)

urlpatterns = [
    path('all-jobs/', job_list, name='job_list'),
    path('jobs/<int:job_id>/', job_detail, name='job_detail'),
    
    path('jobs/<int:job_id>/apply/', apply_job, name='apply_job'),
    path('applications/', employee_applications, name='employee_applications'),
]
