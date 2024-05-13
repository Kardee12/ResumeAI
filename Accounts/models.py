import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Attributes:
        uuid (UUIDField): Unique identifier for the user, generated using uuid.uuid4().
        has_completed_setup (BooleanField): Indicates whether the user has completed the setup process.
        role (CharField): Role of the user, with choices between 'employer' and 'job_searcher'.
        linkedin_url (URLField): URL field for the user's LinkedIn profile.

    Methods:
        __str__: Returns the username of the user.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    has_completed_setup = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices=[('employer', 'Employer'), ('job_searcher', 'Job-Searcher')],
                            null=True, blank=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username
