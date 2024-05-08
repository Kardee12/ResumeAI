from django.contrib import admin
from django.urls import path, include
from Core import views, EmployerViews, JobSearcherViews
from Core import gen_views

urlpatterns = [
    path("", views.index, name='index'),
    path("home/", views.home, name="home"),
    path('settings/',views.settings , name='settings'),
    
    
    #jobsearcher side
    
    path('js-dashboard/', JobSearcherViews.jobsearcher_dashboard, name='jobsearcher_dashboard'),
    #added as of 12:54pm may 3
    path('chat/', JobSearcherViews.jobsearcher_chat, name='jobsearcher_chat'),
    path('js-profile/', JobSearcherViews.jobsearcher_profile, name='jobsearcher_profile'),
    path('js-setup/',JobSearcherViews.js_setup_profile, name='js_setup_profile'),
    path('download-resume/', gen_views.download_resume, name='download-resume'),
    path('edit-jsprofile/', JobSearcherViews.edit_profile, name='edit-profile'),
    # path('edit-job-posting/', EmployerViews.edit_job_posting, name = 'edit_job_posting'),

    
    #employer side
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
