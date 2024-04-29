from django.contrib import admin
from django.urls import path, include
from Core import JobSearcher, EmployerViews, views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employer-dashboard/', EmployerViews.employer_dashboard, name='employer_dashboard'),
    path('jobsearcher-dashboard/', JobSearcher.jobsearcher_dashboard, name='jobsearcher_dashboard'),
]