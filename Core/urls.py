from django.contrib import admin
from django.urls import path, include
from Core import views, EmployerViews, JobSearcherViews
from Core import gen_views

urlpatterns = [
    path("", views.index, name='index'),
    path("home/", views.home, name="home"),
    #dont forget to add job id
    path("em-job-posting/",EmployerViews.jobPostingPage, name="job_posting_page"),
    #add job id -- maybe use jinja? 
    path("em-job-posting-candidatelist/<uuid:job_id>/", EmployerViews.candidatePage ,name="candidate_list"),
    path("emprofile/", EmployerViews.profile, name="employer_profile"),
    path('emdashboard/', EmployerViews.employer_dashboard, name='employer_dashboard'),
    path('js-dashboard/', JobSearcherViews.jobsearcher_dashboard, name='jobsearcher_dashboard'),
    #added as of 12:54pm may 3
    path('chat/', JobSearcherViews.jobsearcher_chat, name='jobsearcher_chat'),
    path('settings/',views.settings , name='settings'),
    path('js-profile/', JobSearcherViews.jobsearcher_profile, name='jobsearcher_profile'),
    path('js-setup/',JobSearcherViews.js_setup_profile, name='js_setup_profile'),
    path('download-resume/', gen_views.download_resume, name='download-resume'),
    path('edit-jsprofile/', JobSearcherViews.edit_profile, name='edit-profile'),
    # path('edit-job-posting/', EmployerViews.edit_job_posting, name = 'edit_job_posting')
    path('emp-setup/', EmployerViews.emp_setupProfile, name='emp_setupProfile'),
    path('employer/dashboard/', EmployerViews.employer_dashboard, name='employer_dashboard')
] 
