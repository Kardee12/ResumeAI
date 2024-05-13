import os

from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from Core.EmployerModel import Job


class UserSkill(models.Model):
    """
    Model representing a user's skill.

    Attributes:
        name (str): name of the skill
        
    Methods:
        __str__: Returns the string representation of the skill (its name).

    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """
    Model representing a user's profile.

    Attributes:
        user (ForeignKey): user associated with the profil
        profile_completed (bool): Indicates whether the user's profile is completed
        location (str): location of the user
        bio (str): professional bio of the user
        resume (ForeignKey): user's resume (linked to the UserResume model)
        skills (ManyToManyField): skills associated with the user

    Methods:
        __str__: Returns string representation of the UserProfile 

    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_completed = models.BooleanField(default=False)
    location = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    resume = models.ForeignKey('UserResume', on_delete=models.SET_NULL, null=True, blank=True, related_name='profile')
    skills = models.ManyToManyField(UserSkill, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class UserResume(models.Model):
    """
    Model representing a user's resume.

    Attributes:
        user (ForeignKey): The user associated with the resume.
        resume (FileField): The file field for uploading the resume.
        uploaded_at (DateTimeField): The date and time when the resume was uploaded.

    Methods:
        __str__: Returns the string representation of the UserResume object.

    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
    resume = models.FileField(
        upload_to='user_resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        blank=True,
        null=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.resume:
            if os.path.isfile(self.resume.path):
                os.remove(self.resume.path)
        super(UserResume, self).delete(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Resume - {self.resume.name if self.resume else 'No resume uploaded'}"


class JobApplication(models.Model):
    """
    Model representing a job application.

    Attributes:
        job (ForeignKey): The job to which the application is submitted.
        user (ForeignKey): The user who submitted the application.
        status (CharField): The status of the application, chosen from predefined choices.
        application_date (DateTimeField): The date and time when the application was submitted.

    Methods:
        __str__: Returns the string representation of the JobApplication object.

    """
    STATUS_CHOICES = (
        ('Applied', 'Applied'),
        ('Interview', 'Interview'),
        ('Offer', 'Offer'),
        ('Rejected', 'Rejected'),
        ('Accepted', 'Accepted'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')
    application_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.job.position} - {self.status}"
