from django.contrib import admin
from .models import JobPost, JobApplication, JobCategory


admin.site.register(JobPost)
admin.site.register(JobApplication)
admin.site.register(JobCategory)
