from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

# Function to check if user is superuser & staff
def is_superuser(user):
    return user.is_authenticated and user.is_staff and user.is_superuser

# Superuser Dashboard View
@login_required
@user_passes_test(is_superuser)
def superuser_dashboard(request):
    return render(request, 'panel/dashboard.html')
