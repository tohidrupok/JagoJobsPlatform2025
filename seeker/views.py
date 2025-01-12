from django.shortcuts import render, get_object_or_404
from .models import Resume

def resume_detail(request, resume_id):
    # Fetch the resume object
    resume = get_object_or_404(Resume, id=resume_id)
    
    # Fetch related data
    educations = resume.educations.all()
    employments = resume.employments.all()
    skills = resume.skills.all()
    projects = resume.projects.all()
    certifications = resume.certifications.all()
    
    # Pass the data to the template
    context = {
        'resume': resume,
        'educations': educations,
        'employments': employments,
        'skills': skills,
        'projects': projects,
        'certifications': certifications,
    }
    return render(request, 'resume_detail.html', context)

def my_resume(request):
    # Fetch the currently logged-in user's resume
    resume = get_object_or_404(Resume, user=request.user)
    
    # Fetch related data
    educations = resume.educations.all()
    employments = resume.employments.all()
    skills = resume.skills.all()
    projects = resume.projects.all()
    certifications = resume.certifications.all()
    
    # Pass the data to the template
    context = {
        'resume': resume,
        'educations': educations,
        'employments': employments,
        'skills': skills,
        'projects': projects,
        'certifications': certifications,
    }
    return render(request, 'resume_detail.html', context) 

def all_resumes(request):
    resumes = Resume.objects.all()
    return render(request, 'all_resume.html', {'resumes': resumes})