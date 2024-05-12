import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    has_completed_setup = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices=[('employer', 'Employer'), ('job_searcher', 'Job-Searcher')],
                            null=True, blank=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username
