from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden



# Create your views here.
@login_required
def employer_dashboard(request):
    if not request.user.is_employer:  
        return HttpResponseForbidden("Access restricted to employers.")
    if not request.user.is_approved:
        return render(request, 'registration/pending_approval.html')
    return render(request, 'employer-profile.html')  


