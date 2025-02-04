from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from accounts.models import EmployerProfile
from .forms import EmployerProfileForm



# Create your views here.
@login_required
def employer_dashboard(request):
    if not request.user.is_employer:  
        return HttpResponseForbidden("Access restricted to employers.")
    if not request.user.is_approved:
        return render(request, 'registration/pending_approval.html')
    return render(request, 'employer-profile.html')   


@login_required
def employer_profile(request):
    if not request.user.is_employer:  
        return HttpResponseForbidden("Access restricted to employers.")
    if not request.user.is_approved:
        return render(request, 'registration/pending_approval.html') 
    
    profile = get_object_or_404(EmployerProfile, user=request.user)
    print(profile)
    return render(request, 'employer-profile.html', {'profile': profile})  


@login_required
def edit_employer_profile(request):
    if not request.user.is_employer:
        return HttpResponseForbidden("Access restricted to employers.")
    
    
    profile = get_object_or_404(EmployerProfile, user=request.user)
    
    if request.method == "POST":
        form = EmployerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('employer_profile')  # Redirect to the profile page after saving
    else:
        form = EmployerProfileForm(instance=profile)
    
    return render(request, 'employer-profile.html', {'form': form})