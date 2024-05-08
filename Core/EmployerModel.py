from django.db import models
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from Core.models import UserProfile
import uuid


class Searcher(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='searcher')

class Job(models.Model):
    job_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    employer_profile = models.ForeignKey('EmployerProfile', on_delete=models.CASCADE, related_name='jobs', null=True)
    applicant_count = models.IntegerField(default=0, editable=False)
    position = models.CharField(max_length=200)
    description = models.TextField()
    pay = models.CharField(max_length=100)
    skills_used = models.ManyToManyField('ResumeSkills')
    company_image_url = models.URLField(max_length=255, blank=True, null=True)
    list_of_applicants = models.ManyToManyField(Searcher, related_name='applied_jobs', blank=True)
    link_to_apply = models.URLField(max_length = 200, blank=True, null=True)
    link_to_company = models.URLField(max_length = 200, blank=True,null=True)
    
    def __str__(self):
        return self.position


class ResumeSkills(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class EmployerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employer_profile')
    position = models.CharField(max_length=120, blank=False, null=False, default='Unknown')
    company_name = models.CharField(max_length=255)
    company_description = models.TextField(blank=True, null=True)
    company_website = models.URLField(max_length=200, blank=True, null=True)
    employer_completed = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.company_name} Profile"

class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    job_searcher = models.ForeignKey(Searcher, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length=50, choices=[('Offer', 'offer'), ('Reject', 'reject'),('Interview', 'interview'), ('Pending', 'pending')],
                            null=True, blank=True)

    def __str__(self):
        return f"{self.job_searcher.user.username} - {self.job.position}"
