from django.shortcuts import render, get_object_or_404, redirect
from .models import JobPost, JobApplication, JobCategory
from .forms import JobApplicationForm, JobPostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db.models import Q


def job_list(request):
    sort_by = request.GET.get('sort_by', 'most_recent')
    show_count = request.GET.get('show_count', 10)
    category_id = request.GET.get('category')
    keyword = request.GET.get('keyword', '').strip()  
    location = request.GET.get('location', '').strip()  
    

    try:
        show_count = int(show_count)
    except ValueError:
        show_count = 10

    #  Fast Filtering with Q Objects
    filters = Q()
    if category_id:
        filters &= Q(job_category_id=category_id)

    # Search kortecha filed ar upor
    if keyword:
        filters &= Q(title__icontains=keyword) | Q(job_description__icontains=keyword) | Q(job_requirements__icontains=keyword)| Q(job_location__icontains=keyword)
    if location:
        
        filters &= Q(job_location__icontains=location)

    job_type_map = {
        "full_time": "Full Time",
        "internship": "Internship",
        "part_time": "Part Time",
        "temporary": "Temporary",
        "contractual": "Contractual"
    }
    if sort_by in job_type_map:
        filters &= Q(job_type=job_type_map[sort_by])

    jobs = JobPost.objects.filter(filters).order_by('-created_at').only(
        "id", "title", "job_category_id", "job_type", "created_at"
    )

    total_jobs = jobs.count()

    paginator = Paginator(jobs, show_count)
    page_number = request.GET.get('page')
    page_jobs = paginator.get_page(page_number)

    # Optimized Category Cache
    categories = cache.get('job_categories')
    if not categories:
        categories = list(JobCategory.objects.values('id', 'name'))
        cache.set('job_categories', categories, timeout=3600)
    

    return render(request, 'jobs/job_list.html', {
        'jobs': page_jobs,
        'total_jobs': total_jobs,
        'sort_by': sort_by,
        'show_count': show_count,
        'category': categories,
        'selected_category': category_id,
        'keyword': keyword, 
        'location': location  
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


