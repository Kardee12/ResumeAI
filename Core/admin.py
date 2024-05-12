from django.contrib import admin

from .EmployerModel import Job, JobSkills
from .models import UserProfile, UserResume


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_completed', 'location', 'bio']
    list_filter = ['profile_completed', 'location']
    search_fields = ['user__username', 'bio']


@admin.register(UserResume)
class UserResumeAdmin(admin.ModelAdmin):
    list_display = ['user', 'resume', 'uploaded_at']
    search_fields = ['user__username']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
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
    list_display = ['name']
    search_fields = ['name']
