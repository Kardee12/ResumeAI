from django.contrib import admin

from .EmployerModel import Job, JobSkills
from .models import UserProfile, UserResume


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing user profiles.
    Attributes:
        list_display (list): contains user's username, profile completion status,
            location, and biography
        list_filter (list): contains profile completion status and location
        search_fields (list): users can search for user profiles based on the username and biography
    """
    list_display = ['user', 'profile_completed', 'location', 'bio']
    list_filter = ['profile_completed', 'location']
    search_fields = ['user__username', 'bio']


@admin.register(UserResume)
class UserResumeAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing user resumes.
    Attributes:
        list_display (list): includes the user's username, resume file, upload timestamp
        search_fields (list): users can for user resumes based on the username
    """
    list_display = ['user', 'resume', 'uploaded_at']
    search_fields = ['user__username']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing job postings.
    Attributes:
        list_display (list): includes the company name, location, position, description,
            pay, link to apply, and company website.
        search_fields (list): Admin can search for job postings based on the company name, location,
            position, description, and company website.
        filter_horizontal (list): filters applicants horizontally 

    Methods:
        get_company_name (function): get the company name associated with a job posting.
        get_company_website (function): get the company website associated with a job posting.
    """
    list_display = ['get_company_name', 'location', 'position', 'description', 'pay', 'link_to_apply',
                    'get_company_website']
    search_fields = ['employer_profile__company_name', 'location', 'position', 'description',
                     'employer_profile__company_website']
    filter_horizontal = ['skills', 'list_of_applicants']

    def get_company_name(self, obj):
        return obj.employer_profile.company_name

    get_company_name.short_description = 'Company Name'
    get_company_name.admin_order_field = 'employer_profile__company_name'  # Allows column order sorting

    def get_company_website(self, obj):
        return obj.employer_profile.company_website

    get_company_website.short_description = 'Company Website'
    get_company_website.admin_order_field = 'employer_profile__company_website'  # Allows column order sorting


@admin.register(JobSkills)
class ResumeSkillsAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing job skills.
    Attributes:
        list_display (list): display list of job skills.
        search_fields (list): Administrators can search for job skills by names.
    """
    list_display = ['name']
    search_fields = ['name']
