from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required()
def jobPostingPage(request):
    return render(request, "Authorized/Employer/JobPostings_Employer.html")

@login_required
def candidatePage(request):
    return render(request, "Authorized/Employer/CandidateList.html")