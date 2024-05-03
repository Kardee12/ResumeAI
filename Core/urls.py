from django.urls import path
from Core import JobSearcher, EmployerViews, views, gen_views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path('emdashboard/', EmployerViews.employer_dashboard, name='employer_dashboard'),
    path('jsdashboard/', JobSearcher.jobsearcher_dashboard, name='jobsearcher_dashboard'),
    path('chat/', JobSearcher.jobsearcher_chat,name='jobsearcher_chat'),
    path('settings/', views.settings,name='settings'),
    path('jsprofile/', JobSearcher.jobsearcher_profile,name='jobsearcher_profile'),
    path('js-setup', JobSearcher.js_setup_profile,name='js_setup_profile1'),
    path('download-resume/', gen_views.download_resume, name='download-resume'),
    path('edit-jsprofile', JobSearcher.edit_profile,name='edit-profile'),
]