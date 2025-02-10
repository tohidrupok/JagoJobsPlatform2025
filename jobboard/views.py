from django.shortcuts import render, get_object_or_404, redirect
from .models import JobPost, JobApplication
from .forms import JobApplicationForm, JobPostForm
from django.contrib.auth.decorators import login_required

def job_list(request):
    jobs = JobPost.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs}) 

def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})

@login_required
def create_job(request):
    if request.method == "POST":
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.poster = request.user  # Assuming the user posting the job is the employer
            job.save()
            return redirect('job_list')
    else:
        form = JobPostForm()
    
    return render(request, 'jobs/create_job.html', {'form': form})


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    seeker = request.user.seeker_profile

    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES, seeker=seeker)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.seeker = seeker
            application.save()
            return redirect('job_detail', job_id=job.id)
    else:
        form = JobApplicationForm(seeker=seeker)

    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})


@login_required
def employee_applications(request):
    applications = JobApplication.objects.filter(job__poster=request.user)
    return render(request, 'jobs/employee_applications.html', {'applications': applications})


