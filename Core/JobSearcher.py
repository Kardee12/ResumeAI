from django.contrib.auth import logout
from django.shortcuts import render

from ResumeAI import settings

def jobsearcher_dashboard(request):
    return render(request, 'Authorized/Core/JobSearcher/dashboard.html')
