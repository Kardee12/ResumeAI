from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from Core.forms import EmployerProfileForm
from Core.models import EmployerProfile, Job
from django.db import transaction



@login_required()
def jobPostingPage(request):
    job  = get_object_or_404(Job, job_uuid)
    return render(request, "Authorized/Employer/JobPostings_Employer.html")

@login_required
def candidatePage(request):
    return render(request, "Authorized/Employer/CandidateList.html")

@login_required
def profile(request):
    user = request.user
    profile = EmployerProfile.objects.get(user=user)
    return render(request,"Authorized/Employer/Profile_Employer.html", context={'profile' : profile})

def setup_employer_profile(request):
    try:
        profile = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            with transaction.atomic():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                return redirect('employer_dashboard')
    else:
        form = EmployerProfileForm(instance=profile)

    return render(request, 'Authorized/Core/Employer/create-employer-profile.html', {'form': form})
                
                

@login_required
def home(request):
    if not request.user.has_completed_setup:
        return redirect('setup')

@login_required
def employer_dashboard(request):
    return render(request, 'Authorized/Core/Employer/dashboard.html')
# make sure to grab dahsboard.html from karthik's branch

