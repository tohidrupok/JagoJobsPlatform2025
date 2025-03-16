from django.urls import path
from .views import superuser_dashboard, delete_profile, job_post_list, publish_job, reject_job, superuser_job_applicants, delete_job_application

urlpatterns = [
    path('dashboard/', superuser_dashboard, name='superuser_dashboard'),
    path('delete-profile/<int:user_id>/', delete_profile, name='delete_profile'),
    path('jobs/', job_post_list, name='job_post_list'),
    path('publish_job/<int:job_id>/', publish_job, name='publish_job'),
    path('reject_job/<int:job_id>/',  reject_job, name='reject_job'),
    path('job/<int:job_id>/applicants/superuser/', superuser_job_applicants, name='superuser_job_applicants'),
    path('delete_job_application/<int:application_id>/', delete_job_application, name='delete_job_application'),
    
]
