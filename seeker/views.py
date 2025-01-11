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

from django.shortcuts import render, get_object_or_404
from .models import Resume

def my_resume(request):
    # Fetch the currently logged-in user's resume
    resume = get_object_or_404(Resume, user=request.user)

    return render(request, 'resume_detail.html', {'resume': resume})