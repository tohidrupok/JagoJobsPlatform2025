from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, SeekerProfile, EmployerProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # Only run this code when a new user is created
        if instance.role == 'seeker':
            SeekerProfile.objects.create(user=instance)
        elif instance.role == 'employer':
            EmployerProfile.objects.create(user=instance)
 
