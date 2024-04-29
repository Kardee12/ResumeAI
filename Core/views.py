from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from Accounts.models import CustomUser

import Accounts.views

def index(request):
    return render(request, "Unauthorized/Core/index.html")

@login_required
def home(request):
    if not request.user.has_completed_setup:
        return redirect('setup')
    user_role = request.user.role
    if user_role == 'job_searcher':
        print("JOB")
        return redirect('jobsearcher_dashboard')
    else:  # Assuming 'employer' or default to this
        print("EMP")
        return redirect('employer_dashboard')


@login_required
def dashboard(request):
    return render(request, "Authorized/Core/JobSearcher/Dashboard.html")