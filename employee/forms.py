from django import forms
from accounts.models import EmployerProfile

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = [
            "company_name",
            "location",
            "company_website",
            "company_description",
            "phone",
            "email",
            "facebook_link",
            "twitter_link",
            "google_link",
            "linkedin_link",
            "founded_date",
            "logo",
        ]
        widgets = {
            # Use a date picker for the founded date field
            'founded_date': forms.DateInput(attrs={'type': 'date'}),
        } 
        
    logo = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
