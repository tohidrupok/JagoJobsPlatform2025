from django.shortcuts import render, get_object_or_404, redirect
from .models import JobPost, JobApplication, JobCategory
from .forms import JobApplicationForm, JobPostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.cache import cache


def job_list(request):
    sort_by = request.GET.get('sort_by', 'most_recent')
    show_count = request.GET.get('show_count', 10)  
    category_id = request.GET.get('category')

    try:
        show_count = int(show_count)
    except ValueError:
        show_count = 10  

    # Get all job posts initially
    jobs = JobPost.objects.all()

    # Apply category filter if selected
    if category_id:
        jobs = jobs.filter(job_category_id=category_id)

    # Apply sorting on the filtered jobs
    if sort_by == "freelance":
        jobs = jobs.filter(job_type="Freelance")
    elif sort_by == "full_time":
        jobs = jobs.filter(job_type="Full Time")
    elif sort_by == "internship":
        jobs = jobs.filter(job_type="Internship")
    elif sort_by == "part_time":
        jobs = jobs.filter(job_type="Part Time")
    elif sort_by == "temporary":
        jobs = jobs.filter(job_type="Temporary")
    elif sort_by == "contractual":
        jobs = jobs.filter(job_type="Contractual")

    # Always order by most recent jobs
    jobs = jobs.order_by('-created_at')

    total_jobs = jobs.count()

    # Pagination
    paginator = Paginator(jobs, show_count)
    page_number = request.GET.get('page')
    page_jobs = paginator.get_page(page_number)

    # Cache job categories for optimization
    categories = cache.get('job_categories')
    if not categories:
        categories = JobCategory.objects.all()
        cache.set('job_categories', categories, timeout=3600)

    return render(request, 'jobs/job_list.html', {
        'jobs': page_jobs,
        'total_jobs': total_jobs,
        'sort_by': sort_by,
        'show_count': show_count,
        'category': categories,
        'selected_category': category_id  
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


