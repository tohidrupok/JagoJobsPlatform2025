from django import forms
from .models import JobApplication, JobPost

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = '__all__'

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['resume']  # Only include resume field

    def __init__(self, *args, **kwargs):
        seeker = kwargs.pop('seeker', None)  # Extract seeker from kwargs
        super().__init__(*args, **kwargs)

        # If the seeker has a profile resume, pre-fill it in the form
        if seeker and seeker.resume:
            self.fields['resume'].initial = seeker.resume