from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from jobboard.models import JobApplication 
from jobboard.models import JobPost
from django.utils import timezone
from accounts.models import CustomUser
from django.contrib import messages

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


@login_required
@user_passes_test(is_superuser)  
def delete_profile(request, user_id):
    
    user = get_object_or_404(CustomUser, id=user_id) 
    print(user)
    if user.is_superuser:
        messages.error(request, "Superuser accounts cannot be deleted.")
        return redirect('superuser_dashboard')

    user.delete()
    print("Delet hoye gacha")
    messages.success(request, f"User {user.username} has been deleted successfully.")
    return redirect('superuser_dashboard')  


@login_required
@user_passes_test(is_superuser)  
def job_post_list(request):
    job_posts = JobPost.objects.all().order_by('-created_at')
    return render(request, 'panel/job_post_list.html', {'job_posts': job_posts})



@login_required
@user_passes_test(is_superuser) 
def publish_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    job.status = 'published'  
    job.save()
    return redirect('job_post_list') 

@login_required
@user_passes_test(is_superuser) 
def reject_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    job.status = 'rejected' 
    job.save()
    return redirect('job_post_list') 


@login_required
@user_passes_test(is_superuser) 
def superuser_job_applicants(request, job_id):

    job = get_object_or_404(JobPost, id=job_id)
    applications = JobApplication.objects.filter(job=job)

    return render(request, 'panel/job_applicants_superuser.html', {
        'job': job,
        'applications': applications,
    }) 
    
    
def delete_job_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    
    if request.user != application.seeker.user and not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete this application.")
        return redirect('home')  

    application.delete()
    messages.success(request, "Job application deleted successfully.")
    return redirect('job_post_list')  

