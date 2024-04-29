from django.contrib import admin
from django.urls import path, include
from Core import NormalViews, views, EmployerViews

urlpatterns = [
    path("", NormalViews.index, name="index"),
    path("dashboard/", views.home, name="home"),
    #dont forget to add job id
    path("employer/job_posting",EmployerViews.jobPostingPage, name="job_posting_page"),
    #add job id -- maybe use jinja? 
    path("employer/job_posting/candidatelist", EmployerViews.candidatePage ,name="candidate_list")
] 
