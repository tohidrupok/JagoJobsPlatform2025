from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from accounts.models import EmployerProfile
from .forms import EmployerProfileForm, JobPostForm
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone


# Create your views here.    
@login_required
def employer_dashboard(request):
    if not request.user.is_employer:  
        return HttpResponseForbidden("Access restricted to employers.")
    if not request.user.is_approved:
        return render(request, 'registration/pending_approval.html')
    
    profile = get_object_or_404(EmployerProfile, user=request.user) 
    return render(request, 'core/dashboard.html', {'profile': profile})   


@login_required
def view_employer_profile(request):
    if not request.user.is_employer:  
        return HttpResponseForbidden("Access restricted to employers.")
    if not request.user.is_approved:
        return render(request, 'registration/pending_approval.html') 
    
    profile = get_object_or_404(EmployerProfile, user=request.user)
    
    total_experience = None
    if profile.founded_date:
        total_experience = timezone.now().year - profile.founded_date.year
        
    return render(request, 'employer-detail-v2.html', {
        'profile': profile,
        'total_experience': total_experience,
    })   
 


# @login_required
# def edit_employer_profile(request):
#     if not request.user.is_employer:
#         return HttpResponseForbidden("Access restricted to employers.")
    
    
#     profile = get_object_or_404(EmployerProfile, user=request.user)
    
#     if request.method == "POST" and request.FILES.get("logo"):
#         profile.logo = request.FILES["logo"]
#         profile.save()
#         return JsonResponse({"success": True, "logo_url": profile.logo.url}) 
    
#     if request.method == "POST":
#         form = EmployerProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('employer_profile')  # Redirect to the profile page after saving
#     else:
#         form = EmployerProfileForm(instance=profile)
    
#     return render(request, 'employer-profile.html', {'form': form, 'profile': profile}) 


@login_required
def employer_profile(request):
    if not request.user.is_employer:
        return HttpResponseForbidden("Access restricted to employers.")
    if not request.user.is_approved:
        return render(request, 'registration/pending_approval.html')
    
    
    profile = get_object_or_404(EmployerProfile, user=request.user)
    
    if request.method == "POST" and request.FILES.get("logo"):
        profile.logo = request.FILES["logo"]
        profile.save()
        return JsonResponse({"success": True, "logo_url": profile.logo.url}) 
    
    if request.method == "POST":
        form = EmployerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('employer_profile')  
    else:
        form = EmployerProfileForm(instance=profile)
    
    return render(request, 'core/dash-company-profile.html', {'form': form, 'profile': profile}) 


from django.contrib import messages 

@login_required
def create_job(request):
    if not request.user.is_employer:
        return HttpResponseForbidden("Access restricted to employers.") 
    if not request.user.is_approved:
        return render(request, 'registration/pending_approval.html')
    
    employer = get_object_or_404(EmployerProfile, user=request.user)  

    if request.method == "POST":
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)  
            job.employee = employer  
            job.save()  
            messages.success(request, "Job posted successfully!")
            return redirect('job_list')  
        else:
            messages.error(request, "Please correct the errors below.")  

    else:
        form = JobPostForm()

    return render(request, 'job/create_job.html', {'form': form, 'profile': employer}) 