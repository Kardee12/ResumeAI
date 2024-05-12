import uuid

from django.conf import settings
from django.db import models


class EmployerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employer_profile')
    position = models.CharField(max_length=120, blank=False, null=False, default='Unknown')
    company_name = models.CharField(max_length=255)
    company_role_description = models.TextField(blank=True, null=True)
    company_website = models.URLField(max_length=200, blank=True, null=True)
    employer_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company_name} Profile"


class JobSkills(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class JobType(models.TextChoices):
    CONTRACTOR = 'Contractor', 'Contractor'
    INTERNSHIP = 'Internship', 'Internship'
    FULL_TIME = 'Full-time', 'Full-time'
    PART_TIME = 'Part-time', 'Part-time'


class Job(models.Model):
    job_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    employer_profile = models.ForeignKey('EmployerProfile', on_delete=models.CASCADE, related_name='jobs', null=True)
    applicant_count = models.IntegerField(default=0, editable=False)
    position = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    pay = models.CharField(max_length=100)
    skills = models.ManyToManyField(JobSkills, blank=True)
    list_of_applicants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='applied_jobs', blank=True)
    link_to_apply = models.URLField(max_length=200, blank=True, null=True)
    job_type = models.CharField(max_length=20, choices=JobType.choices, default=JobType.FULL_TIME)

    def __str__(self):
        return self.position
