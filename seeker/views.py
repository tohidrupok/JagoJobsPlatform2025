from django.shortcuts import render, redirect, get_object_or_404
from .models import Resume, Education, Employment, Skill, Project, Certification
from .forms import ResumeForm, EducationForm, EmploymentForm, SkillForm, ProjectForm, CertificationForm, SeekerProfileForm, PersonalDetailsForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from accounts.models import SeekerProfile
from datetime import date


@login_required
def resume_detail(request, resume_id):

    resume = get_object_or_404(Resume, id=resume_id)
    
    # Fetch related data
    educations = resume.educations.all()
    employments = resume.employments.all()
    skills = resume.skills.all()
    projects = resume.projects.all()
    certifications = resume.certifications.all()

    context = {
        'resume': resume,
        'educations': educations,
        'employments': employments,
        'skills': skills,
        'projects': projects,
        'certifications': certifications,
    }
    return render(request, 'resume_detail.html', context) 


@login_required
def my_resume(request):
    
    resume = get_object_or_404(Resume, user=request.user)
    
    if request.method == "POST" and request.FILES.get("logo"):
        resume.image = request.FILES["logo"]
        resume.save()
        return JsonResponse({"success": True, "logo_url": resume.image.url}) 
    
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('my_resume')  
    else:
        form = ResumeForm(instance=resume) 
            
    # Fetch related data
    educations = resume.educations.all().order_by('-id')
    employments = resume.employments.all().order_by('-id')
    skills = resume.skills.all().order_by('-id')
    projects = resume.projects.all().order_by('-id')
    certifications = resume.certifications.all().order_by('-id')
    

    context = {
        'form': form,
        'resume': resume,
        'educations': educations,
        'employments': employments,
        'skills': skills,
        'projects': projects,
        'certifications': certifications,
        
        
    }
    return render(request, 'resume_detail.html', context) 

# @login_required
# def seeker_profile(request):
   
#     resume = get_object_or_404(Resume, user=request.user)
    
#     if request.method == "POST" and request.FILES.get("logo"):
#         resume.image = request.FILES["logo"]
#         resume.save()
#         return JsonResponse({"success": True, "logo_url": resume.image.url}) 
    
#     if request.method == "POST":
#         form = ResumeForm(request.POST, request.FILES, instance=resume)
#         if form.is_valid():
#             form.save()
#             return redirect('employer_profile')  
#     else:
#         form = ResumeForm(instance=resume)
    
#     return render(request, 'resume_detail.html', {'form': form, 'resume': resume}) 

@login_required
def all_resumes(request):
    resumes = Resume.objects.all()
    return render(request, 'all_resume.html', {'resumes': resumes}) 


@login_required
def edit_resume(request):
    resume = get_object_or_404(Resume, user=request.user)
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('my_resume')
    else:
        form = ResumeForm(instance=resume)
    return render(request, 'edit.html', {'form': form,'resume': resume })

@login_required
def edit_education(request, pk):
    education = get_object_or_404(Education, pk=pk)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect('my_resume')
    else:
        form = EducationForm(instance=education)
    resume = get_object_or_404(Resume, user=request.user)
    return render(request, 'edit.html', {'form': form,'resume': resume })

@login_required
def delete_education(request, pk):
    education = get_object_or_404(Education, pk=pk)

    if request.method == 'POST':
        education.delete()
        return redirect('my_resume')  

    return redirect('my_resume') 

@login_required
def delete_employment(request, pk):
    employment = get_object_or_404(Employment, pk=pk)

    if request.method == 'POST':
        employment.delete()
        return redirect('my_resume')  

    return redirect('my_resume')

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('my_resume')  

    return redirect('my_resume')

@login_required
def delete_certification(request, pk):
    certification = get_object_or_404(Certification, pk=pk)

    if request.method == 'POST':
        certification.delete()
        return redirect('my_resume')  

    return redirect('my_resume')

@login_required
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk)

    if request.method == 'POST':
        skill.delete()
        return redirect('my_resume')  

    return redirect('my_resume')

@login_required
def edit_employment(request, pk):
    employment = get_object_or_404(Employment, pk=pk)
    resume = get_object_or_404(Resume, user=request.user)
    
    if request.method == 'POST':
        form = EmploymentForm(request.POST, instance=employment)
        if form.is_valid():
            form.save()
            return redirect('my_resume')
    else:
        form = EmploymentForm(instance=employment)
        
    return render(request, 'edit.html', {'form': form,'resume': resume })

@login_required
def edit_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    resume = get_object_or_404(Resume, user=request.user)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('my_resume')
    else:
        form = SkillForm(instance=skill)
        
    return render(request, 'edit.html', {'form': form,'resume': resume })

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    resume = get_object_or_404(Resume, user=request.user) 
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('my_resume')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'edit.html', {'form': form,'resume': resume })

@login_required
def edit_certification(request, pk):
    certification = get_object_or_404(Certification, pk=pk)
    resume = get_object_or_404(Resume, user=request.user)
    
    if request.method == 'POST':
        form = CertificationForm(request.POST, instance=certification)
        if form.is_valid():
            form.save()
            return redirect('my_resume')
    else:
        form = CertificationForm(instance=certification)
    return render(request, 'edit.html', {'form': form,'resume': resume })

#ADD New Object
@login_required
def add_education(request):
    resume = Resume.objects.get(user=request.user)  
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.resume = resume  
            education.save()
            return redirect('my_resume')  
    else:
        form = EducationForm()
    return render(request, 'edit.html', {'form': form}) 

@login_required
def add_employment(request):
    resume = Resume.objects.get(user=request.user)
    if request.method == 'POST':
        form = EmploymentForm(request.POST)
        if form.is_valid():
            employment = form.save(commit=False)
            employment.resume = resume
            employment.save()
            return redirect('my_resume')
    else:
        form = EmploymentForm()
    return render(request, 'edit.html', {'form': form}) 

@login_required
def add_skill(request):
    resume = Resume.objects.get(user=request.user)
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.resume = resume
            skill.save()
            return redirect('my_resume')
    else:
        form = SkillForm()
    return render(request, 'edit.html', {'form': form}) 


@login_required
def add_project(request):
    resume = Resume.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.resume = resume
            project.save()
            return redirect('my_resume')
    else:
        form = ProjectForm()
    return render(request, 'edit.html', {'form': form}) 


@login_required
def add_certification(request):
    resume = Resume.objects.get(user=request.user)
    if request.method == 'POST':
        form = CertificationForm(request.POST)
        if form.is_valid():
            certification = form.save(commit=False)
            certification.resume = resume
            certification.save()
            return redirect('my_resume')
    else:
        form = CertificationForm()
    return render(request, 'edit.html', {'form': form})  


#upload resume
@login_required
def upload_resume(request):
    
    resume = get_object_or_404(Resume, user=request.user)
    profile = SeekerProfile.objects.get(user=request.user)
    
    if request.method == "POST":
        form = SeekerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile') 

    else:
        form = SeekerProfileForm(instance=profile)

    return render(request, 'upload_resume.html', {'form': form, 'resume': resume })





@login_required
def view_profile(request):
    """View profile based on the user's role."""
    
    if request.user.is_seeker:
        profile = get_object_or_404(SeekerProfile, user=request.user)
        resume = get_object_or_404(Resume, user=request.user)
        age = None
        if resume.date_of_birth:
            today = date.today()
            age = today.year - resume.date_of_birth.year - (
                (today.month, today.day) < (resume.date_of_birth.month, resume.date_of_birth.day)
            )

        # Fetch related data
        educations = resume.educations.all().order_by('-id')
        employments = resume.employments.all().order_by('-id')
        skills = resume.skills.all().order_by('-id')
        projects = resume.projects.all().order_by('-id')
        certifications = resume.certifications.all().order_by('-id')
        total_years_of_experience = sum([employment.duration() for employment in employments])
        print("Total yearts of ",total_years_of_experience)
        
        
        template = 'seeker-detail.html'
    else:
        return redirect('home')
    
    context = {
            'profile': profile,
            'resume': resume,
            'educations': educations,
            'employments': employments,
            'skills': skills,
            'projects': projects,
            'certifications': certifications,
            'age': age,
            'total_years_of_experience': total_years_of_experience,
        }
    
    return render(request, template, context)


@login_required
def edit_profile(request):
    """Edit profile based on the user's role."""

    if request.user.is_seeker:
        profile = get_object_or_404(SeekerProfile, user=request.user)
        form_class = SeekerProfileForm
        template = 'edit_profile.html'
    else:
        return redirect('home')
    
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = form_class(instance=profile)
    
    return render(request, template, {'form': form}) 



# def view_profile(request):
#     """View profile based on the user's role."""
#     if request.user.is_seeker:
#         profile = get_object_or_404(SeekerProfile, user=request.user)
#         template = 'seeker-detail.html'
#     else:
#         return redirect('home')
    
#     return render(request, template, {'profile': profile}) 



#Personal data's views

from django.http import JsonResponse
def edit_personal_details(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    data = {
        "name": resume.name,
        "title": resume.title,
        "date_of_birth": resume.date_of_birth.strftime('%Y-%m-%d') if resume.date_of_birth else "",
        "permanent_address": resume.permanent_address,
        "gender": resume.gender,
        "email": resume.email,
        "phone_number": resume.phone_number,
        
        "area_pin_code": resume.area_pin_code,
        "marital_status": resume.marital_status,
        "hometown": resume.hometown,
        "languages": resume.languages,
    }
    return JsonResponse(data) 

def update_personal_details(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)

    if request.method == "POST":
        form = PersonalDetailsForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            messages.success(request, "Personal details updated successfully!")  # Success message
            return redirect("my_resume")  # Redirect to 'my_resume' page
        else:
            messages.error(request, "Error updating details. Please check your inputs.")  # Error message

    return redirect("my_resume") 