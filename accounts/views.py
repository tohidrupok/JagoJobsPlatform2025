from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import SeekerRegistrationForm, EmployerRegistrationForm, CustomLoginForm, ManagerRegistrationForm
from .models import CustomUser

def home(request):
    return render(request, 'index.html')  


def register(request):
    seeker_form = SeekerRegistrationForm()
    employer_form = EmployerRegistrationForm()

    if request.method == 'POST':
        if 'seeker_submit' in request.POST:
            print("candidate")
            seeker_form = SeekerRegistrationForm(request.POST)
            if seeker_form.is_valid():
                user = seeker_form.save(commit=False)
                user.role = 'seeker'
                user.save()
                login(request, user)
                return redirect('seeker_dashboard')
        elif 'employer_submit' in request.POST:
            employer_form = EmployerRegistrationForm(request.POST)
            if employer_form.is_valid():
                user = employer_form.save(commit=False)
                user.role = 'employer'
                user.is_approved = False
                user.save()
                return render(request, 'registration/pending_approval.html')

    return render(request, 'base.html', {
        'seeker_form': seeker_form,
        'employer_form': employer_form
    }) 
    
    

def register_seeker(request):
    if request.method == 'POST':
        form = SeekerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'seeker'
            user.save()
            login(request, user)  
            return redirect('seeker_dashboard')
    else:
        form = SeekerRegistrationForm()
    return render(request, 'registration/register_seeker.html', {'form': form})

def register_employer(request):
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'employer'
            user.is_approved = False  
            user.save()
            return render(request, 'registration/pending_approval.html')
    else:
        form = EmployerRegistrationForm()
    return render(request, 'registration/register_employer.html', {'form': form})

def register_manager(request):
    if request.method == 'POST':
        form = ManagerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'manager'
            user.is_approved = False  
            user.save()
            return render(request, 'manager/pending_approval.html')
    else:
        form = ManagerRegistrationForm()
    return render(request, 'manager/register_manager.html', {'form': form}) 


def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_manager and not user.is_approved:
                    return render(request, 'registration/pending_approval.html')
                if user.is_manager:
                    return redirect('manager_dashboard')
                elif user.is_employer:
                    return redirect('employer_dashboard')
                elif user.is_seeker:
                    return redirect('seeker_dashboard')
    else:
        form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def custom_logout(request):
    logout(request)
    return redirect('custom_login')

# Dashboards
@login_required
def seeker_dashboard(request):
    if not request.user.is_seeker:  
        return HttpResponseForbidden("Access restricted to job seekers.")
    return render(request, 'seeker/dashboard.html')

@login_required
def employer_dashboard(request):
    if not request.user.is_employer:  
        return HttpResponseForbidden("Access restricted to employers.")
    if not request.user.is_approved:
        return render(request, 'registration/pending_approval.html')
    return render(request, 'employer/dashboard.html')

@login_required
def manager_dashboard(request):
    if not request.user.is_manager:
        return HttpResponseForbidden("Access restricted to managers.")
    if not request.user.is_approved:
        return render(request, 'registration/pending_approval.html')
    return render(request, 'manager/dashboard.html')  







#####################
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

def employee_required(view_func):
    @user_passes_test(lambda u: u.is_authenticated and u.is_manager)
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@employee_required
def approve_manager_list(request):
    """List all pending manager approval requests."""
    pending_managers = CustomUser.objects.filter(role='employer', is_approved=False)
    print(pending_managers)
    return render(request, 'manager/approve_manager_list.html', {'pending_managers': pending_managers})

@login_required
@employee_required
def approve_manager(request, user_id):
    """Approve a specific manager."""
    manager = get_object_or_404(CustomUser, id=user_id, role='employer', is_approved=False)
    
    if request.method == 'POST':
        manager.is_approved = True
        manager.save()
        return redirect('approve_manager_list')

    return render(request, 'manager/approve_manager.html', {'manager': manager}) 
