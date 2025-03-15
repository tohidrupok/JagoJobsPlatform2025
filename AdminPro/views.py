from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from jobboard.models import JobApplication 
from jobboard.models import JobPost
from django.utils import timezone

# Function to check if user is superuser & staff
def is_superuser(user):
    return user.is_authenticated and user.is_staff and user.is_superuser

# Superuser Dashboard View
@login_required
@user_passes_test(is_superuser)
def superuser_dashboard(request): 
    
    job_posts = JobPost.objects.all()
    job_count = job_posts.count()  
    application_count = JobApplication.objects.all().count()
    recent_job_applications = JobApplication.objects.all().order_by('-applied_at')[:8]
    today_job_posts = JobPost.objects.filter(created_at__date=timezone.now().date()).count() 
    today_applications = JobApplication.objects.filter(applied_at__date=timezone.now().date()).count() 
    
    return render(request, 'panel/dashboard.html', {

        'job_count': job_count,
        'application_count': application_count,
        
        'today_job_posts': today_job_posts,
        'today_applications': today_applications,
        'recent_job_applications':recent_job_applications
    })

