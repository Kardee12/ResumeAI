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

    path('jobsearcher/dashboard', JobSearcher.jobsearcher_dashboard, name='jobsearcher_dashboard'),
    path('jobsearcher/chat/', JobSearcher.jobsearcher_chat, name='jobsearcher_chat'),
    path('jobsearcher/settings/', views.settings, name='settings'),
    path('jobsearcher/profile/', JobSearcher.jobsearcher_profile, name='jobsearcher_profile'),
    path('js-setup/', JobSearcher.js_setup_profile, name='js_setup_profile'),
    path('jobsearcher/download-resume/', gen_views.download_resume, name='download-resume'),
    path('jobsearcher/profile/edit', JobSearcher.edit_profile, name='edit-profile'),
    path('jobsearcher/create-resume/', JobSearcher.create_resume, name='create-resume'),
    path('jobsearcher/profile/update-skills/', JobSearcher.update_skills, name='update_skills'),
    path('jobsearcher/chat/processMessages/', JobSearcher.processMessages, name='processMessages'),
    path('jobsearcher/chat/clearchat/', JobSearcher.clearChat, name='clearChat'),
    path('jobsearcher/search', JobSearcher.search, name='search'),
    path('jobsearcher/apply-for-job/', JobSearcher.apply_for_job, name='apply_for_job'),
    path('jobsearcher/all-job-applications/',JobSearcher.all_job_apps, name='all_job_apps'),

    path('emp-setup/', EmployerViews.emp_setupProfile, name='emp_setupProfile'),
    path("employer/job_posting/",EmployerViews.job_posting_page, name="job_posting_page"),
    path("employer/<uuid:job_id>/candidate_list", EmployerViews.candidatePage ,name="candidate_list"),
    path("employer/profile/", EmployerViews.profile, name="employer_profile"),
    path('employer/settings/', views.empsettings, name='empsettings'),
    path('employer/profile/edit', EmployerViews.edit_employer_profile, name='edit_employer_profile'),
    path('employer/job-posting-page', EmployerViews.job_posting_page, name = 'job_posting_page'),
    path('employer/create-job-posting', EmployerViews.create_job_posting, name='create_job_posting'),
    path('employer/dashboard/', EmployerViews.employer_dashboard, name='employer_dashboard'),
    path('employer/company/page', EmployerViews.company_profile_page, name='company_profile_page'),
    path('employer/company/edit/page', EmployerViews.edit_company_page, name='edit_company_page'),
    path('update-status/<int:application_id>/', EmployerViews.update_candidate_status, name='update_candidate_status'),
    path('employer/edit-job/<uuid:job_id>/', EmployerViews.edit_job_posting, name='edit_job_posting'),
    path('employer/delete-job/<uuid:job_id>/', EmployerViews.delete_job, name='delete_job'),

]
