from django.contrib import admin
from django.urls import path, include
<<<<<<< HEAD
from Core import views, EmployerViews, JobSearcherViews
=======
from Core import views, EmployerViews, JobSearcher
>>>>>>> origin/Karthik
from Core import gen_views

urlpatterns = [
    path("", views.index, name='index'),
    path("home/", views.home, name="home"),
<<<<<<< HEAD
    #dont forget to add job id
    path("em-job-posting/",EmployerViews.jobPostingPage, name="job_posting_page"),
    #add job id -- maybe use jinja? 
    path("em-job-posting-candidatelist/", EmployerViews.candidatePage ,name="candidate_list"),
    path("emprofile/", EmployerViews.profile, name="employer_profile"),
    path("edit-emprofile/", EmployerViews.edit_profile, name="edit_profile"),
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
    path('emp-setup/', EmployerViews.emp_setupProfile, name='emp_setupProfile')
=======
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
    path('apply-for-job/', JobSearcher.apply_for_job, name='apply_for_job'),

    path('emp-setup/', EmployerViews.emp_setupProfile, name='emp_setupProfile'),
    path("employer/job_posting/",EmployerViews.job_posting_page, name="job_posting_page"),
    path("employer/<uuid:job_id>/candidate_list", EmployerViews.candidatePage ,name="candidate_list"),
    path("employer/profile/", EmployerViews.profile, name="employer_profile"),
    path('employer/job-posting-page', EmployerViews.job_posting_page, name = 'job_posting_page'),
    path('employer/create-job-posting', EmployerViews.create_job_posting, name='create_job_posting'),
    path('employer/dashboard/', EmployerViews.employer_dashboard, name='employer_dashboard'),
    path('employer/company/page', EmployerViews.company_profile_page, name='company_profile_page'),
    path('employer/company/edit/page', EmployerViews.edit_company_page, name='edit_company_page')
>>>>>>> origin/Karthik
] 
