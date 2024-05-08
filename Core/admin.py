from django.contrib import admin
from .models import UserProfile, UserResume
from .EmployerModel import Job, JobSkills

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
    list_display = ['position', 'description', 'pay', 'company_image_url','link_to_apply', 'link_to_company']
    search_fields = ['position','description']
    filter_horizontal = ['skills', 'list_of_applicants']
@admin.register(JobSkills)
class ResumeSkillsAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']