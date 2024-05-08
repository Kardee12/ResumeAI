from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from allauth.socialaccount.models import SocialAccount
import uuid

<<<<<<< HEAD
class UserSkill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name

=======
from Core.EmployerModel import Job


class UserSkill(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


>>>>>>> origin/Karthik
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_completed = models.BooleanField(default=False)
    location = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    resume = models.ForeignKey('UserResume', on_delete=models.SET_NULL, null=True, blank=True, related_name='profile')
    skills = models.ManyToManyField(UserSkill, blank=True)
<<<<<<< HEAD
    goal = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.user.username}'s Profile"

=======

    def __str__(self):
        return f"{self.user.username}'s Profile"


>>>>>>> origin/Karthik
class UserResume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
    resume = models.FileField(
        upload_to='user_resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        blank=True,
        null=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Resume - {self.resume.name if self.resume else 'No resume uploaded'}"
<<<<<<< HEAD
    
=======


class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    application_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.job.position} - {self.status}"
>>>>>>> origin/Karthik
