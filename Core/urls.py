from django.contrib import admin
from django.urls import path, include
from Core import views, EmployerViews, JobSearcher
from Core import gen_views

urlpatterns = [
    path("", views.index, name='index'),
    path("home/", views.home, name="home"),
    path('custom-logout/', views.custom_logout, name='custom_logout'),
    path('logout/', views.logoutView, name='logout'),
    path("login/", views.logView.as_view(), name='login'),

    path('jsdashboard/', JobSearcher.jobsearcher_dashboard, name='jobsearcher_dashboard'),
    path('chat/', JobSearcher.jobsearcher_chat, name='jobsearcher_chat'),
    path('settings/', views.settings, name='settings'),
    path('jsprofile/', JobSearcher.jobsearcher_profile, name='jobsearcher_profile'),
    path('js-setup/', JobSearcher.js_setup_profile, name='js_setup_profile'),
    path('download-resume/', gen_views.download_resume, name='download-resume'),
    path('edit-jsprofile/', JobSearcher.edit_profile, name='edit-profile'),
    path('create-resume/', JobSearcher.create_resume, name='create-resume'),
    path('jsprofile/update-skills/', JobSearcher.update_skills, name='update_skills'),
    path('chat/processMessages/', JobSearcher.processMessages, name='processMessages'),
    path('chat/clearchat/', JobSearcher.clearChat, name='clearChat'),
    path('search/', JobSearcher.search, name='search'),

    path('emp-setup/', EmployerViews.emp_setupProfile, name='emp_setupProfile'),
    path("employer/job_posting/",EmployerViews.job_posting_page, name="job_posting_page"),
    path("employer/<uuid:job_id>/candidate_list", EmployerViews.candidatePage ,name="candidate_list"),
    path("employer/profile/", EmployerViews.profile, name="employer_profile"),
    path('employer/job-posting-page', EmployerViews.job_posting_page, name = 'job_posting_page'),
    path('employer/create-job-posting', EmployerViews.create_job_posting, name='create_job_posting'),
    path('employer/dashboard/', EmployerViews.employer_dashboard, name='employer_dashboard'),
    path('employer/company/page', EmployerViews.company_profile_page, name='company_profile_page'),
    path('employer/company/edit/page', EmployerViews.edit_company_page, name='edit_company_page')
] 
