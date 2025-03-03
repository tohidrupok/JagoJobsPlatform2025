from django.shortcuts import render, get_object_or_404, redirect
from .models import JobPost, JobApplication, JobCategory
from .forms import JobApplicationForm, JobPostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db.models import Q
from django.utils.timezone import now, timedelta


def job_list(request):
    sort_by = request.GET.get('sort_by', 'most_recent')
    show_count = request.GET.get('show_count', 10)
    category_id = request.GET.get('category')
    keyword = request.GET.get('keyword', '').strip()
    location = request.GET.get('location', '').strip()
    date_filter = request.GET.get('date_filter', '')  
    
    # Check if user clicked "Remove" on a filter
    if 'remove_category' in request.GET:
        category_id = ''
    if 'remove_keyword' in request.GET:
        keyword = ''
    if 'remove_location' in request.GET:
        location = ''
    if 'remove_date' in request.GET:
        date_filter = ''

    # Check if "Clear All" was clicked
    if 'clear_all' in request.GET:
        category_id = keyword = location = date_filter = ''
        

    try:
        show_count = int(show_count)
    except ValueError:
        show_count = 10

 
    filters = Q()
    if category_id:
        filters &= Q(job_category_id=category_id)


    if keyword:
        filters &= Q(title__icontains=keyword) | Q(job_description__icontains=keyword) | Q(job_requirements__icontains=keyword)


    if location:
        filters &= Q(job_location__icontains=location)

    today = now().date()
    if date_filter:
        if date_filter == "today":
            filters &= Q(application_deadline=today)
        elif date_filter == "last_hour":
            filters &= Q(created_at__gte=now() - timedelta(hours=1))
        elif date_filter == "last_24_hours":
            filters &= Q(created_at__gte=now() - timedelta(days=1))
        elif date_filter == "last_7_days":
            filters &= Q(created_at__gte=now() - timedelta(days=7))
        elif date_filter == "last_14_days":
            filters &= Q(created_at__gte=now() - timedelta(days=14))
        elif date_filter == "last_30_days":
            filters &= Q(created_at__gte=now() - timedelta(days=30))

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
        "id", "title", "job_category_id", "job_type", "job_location", "created_at"
    )

    total_jobs = jobs.count()
    query_params = request.GET.copy()

    # Paginate 
    paginator = Paginator(jobs, show_count)
    page_number = request.GET.get('page')
    page_jobs = paginator.get_page(page_number)

    #Cached Categories
    categories = cache.get('job_categories')
    if not categories:
        categories = list(JobCategory.objects.values('id', 'name'))
        cache.set('job_categories', categories, timeout=3600)

    date_filter_options = {
        "today": "Today Deadline",
        "last_hour": "Last hour",
        "last_24_hours": "Last 24 hours",
        "last_7_days": "Last 7 days",
        "last_14_days": "Last 14 days",
        "last_30_days": "Last 30 days",
        "all jobs": "All"
    }

    return render(request, 'jobs/job_list.html', {
        'jobs': page_jobs,
        'total_jobs': total_jobs,
        'sort_by': sort_by,
        'show_count': show_count,
        'category': categories,
        'selected_category': category_id,
        'keyword': keyword,
        'location': location,
        'date_filter_options': date_filter_options,  
        'selected_date_filter': date_filter ,
        'query_params': query_params
    })


def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    seeker = request.user.seeker_profile if request.user.is_authenticated and hasattr(request.user, 'seeker_profile') else None
    related_jobs = JobPost.objects.filter(job_category=job.job_category).exclude(id=job.id).order_by('-created_at')[:9]
    has_applied = JobApplication.objects.filter(job=job, seeker=seeker).exists() if seeker else False

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'seeker': seeker,
        'related_jobs': related_jobs,
        'has_applied': has_applied
    })
    

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


from django.http import JsonResponse
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    seeker = request.user.seeker_profile
    
    if JobApplication.objects.filter(job=job, seeker=seeker).exists():
        return JsonResponse({"success": False, "error": "You have already applied for this job."})
 
 
    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES, seeker=seeker)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.seeker = seeker
            application.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "Invalid form submission."})

    return JsonResponse({"success": False, "error": "Invalid request."})


@login_required
def employee_applications(request):
    applications = JobApplication.objects.filter(job__poster=request.user)
    return render(request, 'jobs/employee_applications.html', {'applications': applications})


