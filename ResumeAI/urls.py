"""
URL configuration for ResumeAI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from ResumeAI import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("Core.urls")),
    path("accounts/", include("Accounts.urls"))
]

if not settings.DEBUG:
    handler403 = 'Core.views.permission_denied'
