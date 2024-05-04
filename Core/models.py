from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from allauth.socialaccount.models import SocialAccount

class UserSkill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_completed = models.BooleanField(default=False)
    location = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    resume = models.ForeignKey('UserResume', on_delete=models.SET_NULL, null=True, blank=True, related_name='profile')
    skills = models.ManyToManyField(UserSkill, blank=True)
    goal = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.user.username}'s Profile"

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
    
#employer side

class Job(models.Model):
    position = models.CharField(max_length = 200)
    description = models.TextField()
    pay = models.CharField(max_length = 100)
    skills_used = models.ManyToManyField('ResumeSkills')
    company_image_url = models.URLField(max_length=255, blank=True, null=True)
    list_of_applicants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='applied_jobs', blank=True)
    link_to_apply = models.URLField(max_length = 200, blank=True, null=True)
    link_to_company = models.URLField(max_length = 200, blank=True,null=True)
    
    def __str__(self):
        return self.position
    
class ResumeSkills(models.Model):
    name = models.CharField(max_length = 120, unique=True)
    
    def __str__(self):
        return self.name