from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required()
def jobPostingPage(request):
    return render(request, "Authorized/Employer/JobPostings_Employer.html")

@login_required
def candidatePage(request):
    return render(request, "Authorized/Employer/CandidateList.html")

@login_required
def profile(request):
    return render(request,"Authorized/Employer/Profile_Employer.html")

@login_required
def home(request):
    if not request.user.has_completed_setup:
        return redirect('setup')

@login_required
def employer_dashboard(request):
    return render(request, 'Authorized/Core/Employer/dashboard.html')
# make sure to grab dahsboard.html from karthik's branch