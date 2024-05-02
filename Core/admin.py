from django.contrib import admin
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