from django.shortcuts import render, get_object_or_404, redirect
from .models import JobPost, JobApplication, JobCategory
from .forms import JobApplicationForm, JobPostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def job_list(request):
  
    sort_by = request.GET.get('sort_by', 'most_recent')
    show_count = request.GET.get('show_count', 10)  

    
    try:
        show_count = int(show_count)
    except ValueError:
        show_count = 10  

    # Sorting logic
    if sort_by == "freelance":
        jobs = JobPost.objects.filter(job_type="Freelance").order_by('-created_at') 
    elif sort_by == "full_time":
        jobs = JobPost.objects.filter(job_type="Full Time").order_by('-created_at') 
    elif sort_by == "internship":
        jobs = JobPost.objects.filter(job_type="Internship").order_by('-created_at') 
    elif sort_by == "part_time":
        jobs = JobPost.objects.filter(job_type="Part Time").order_by('-created_at') 
    elif sort_by == "temporary":
        jobs = JobPost.objects.filter(job_type="Temporary").order_by('-created_at') 
    elif sort_by == "contractual":
        jobs = JobPost.objects.filter(job_type="Contractual").order_by('-created_at') 
    else:
        jobs = JobPost.objects.all().order_by('-created_at').order_by('-created_at') 

    total_jobs = jobs.count()  

    # Pagination
    paginator = Paginator(jobs, show_count)  
    page_number = request.GET.get('page')
    page_jobs = paginator.get_page(page_number) 
    
    
    category = JobCategory.objects.all()
 
    return render(request, 'jobs/job_list.html', {
        'jobs': page_jobs,
        'total_jobs': total_jobs,
        'sort_by': sort_by,
        'show_count': show_count,
        
        'category': category
    })



def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})

@login_required
def create_job(request):
    if request.method == "POST":
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.poster = request.user  
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


