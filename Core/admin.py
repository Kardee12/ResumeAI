from django.contrib import admin
from .models import UserProfile, UserResume
from .EmployerModel import Job, ResumeSkills, EmployerProfile, Searcher, JobApplication

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_completed', 'location', 'bio']
    list_filter = ['profile_completed', 'location']
    search_fields = ['user__username', 'bio']
@admin.register(UserResume)
class UserResumeAdmin(admin.ModelAdmin):
    list_display = ['user', 'resume', 'uploaded_at']
    search_fields = ['user__username']
@admin.register(Searcher)
class SearcherAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'position', 'company_website', 'contact_email')
    list_filter = ('company_name', 'position')
    search_fields = ('company_name', 'user__username')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('position', 'employer_profile', 'pay', 'applicant_count')
    list_filter = ('position', 'pay', 'employer_profile__company_name')
    search_fields = ('position', 'description', 'employer_profile__company_name')
    filter_horizontal = ('skills_used',)
    
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'job_searcher', 'application_date', 'status')
    list_filter = ('status', 'job__position')
    search_fields = ('job__position', 'job_searcher__user__username')

@admin.register(ResumeSkills)
class ResumeSkillsAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']