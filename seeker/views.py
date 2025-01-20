from django.shortcuts import render, redirect, get_object_or_404
from .models import Resume, Education, Employment, Skill, Project, Certification
from .forms import ResumeForm, EducationForm, EmploymentForm, SkillForm, ProjectForm, CertificationForm


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


def my_resume(request):
    print("dukcha")
    resume = get_object_or_404(Resume, user=request.user)
    
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

def all_resumes(request):
    resumes = Resume.objects.all()
    return render(request, 'all_resume.html', {'resumes': resumes}) 



def edit_resume(request):
    resume = get_object_or_404(Resume, user=request.user)
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('my_resume')
    else:
        form = ResumeForm(instance=resume)
    return render(request, 'edit.html', {'form': form})

def edit_education(request, pk):
    education = get_object_or_404(Education, pk=pk)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect('my_resume')
    else:
        form = EducationForm(instance=education)
    return render(request, 'edit.html', {'form': form})

def edit_employment(request, pk):
    employment = get_object_or_404(Employment, pk=pk)
    if request.method == 'POST':
        form = EmploymentForm(request.POST, instance=employment)
        if form.is_valid():
            form.save()
            return redirect('my_resume')
    else:
        form = EmploymentForm(instance=employment)
    return render(request, 'edit.html', {'form': form})

def edit_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('my_resume')
    else:
        form = SkillForm(instance=skill)
    return render(request, 'edit.html', {'form': form})

def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('my_resume')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'edit.html', {'form': form})

def edit_certification(request, pk):
    certification = get_object_or_404(Certification, pk=pk)
    if request.method == 'POST':
        form = CertificationForm(request.POST, instance=certification)
        if form.is_valid():
            form.save()
            return redirect('my_resume')
    else:
        form = CertificationForm(instance=certification)
    return render(request, 'edit.html', {'form': form})

#ADD New Object

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


