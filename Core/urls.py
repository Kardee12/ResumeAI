from django.contrib import admin
from django.urls import path, include
from Core import NormalViews, views

urlpatterns = [
    path("", NormalViews.index, name="index"),
    path("dashboard/", views.home, name="home")
]
