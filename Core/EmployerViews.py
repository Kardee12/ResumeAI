from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from ResumeAI import settings
from ResumeAI.Generic.generic_decoraters import employer_required
from Core.EmployerForms import EmployerProfileForm
from Core.EmployerModel import EmployerProfile, Job
from django.db import transaction


@login_required
@employer_required
def emp_setupProfile(request):
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                profile, created = EmployerProfile.objects.get_or_create(user = request.user)
                profile.company_name = form.cleaned_data['company_name']
                profile.company_description = form.cleaned_data['company_description']
                profile.company_website = form.cleaned_data['company_website']
                profile.contact_email = form.cleaned_data['contact_email']
                profile.save()
            return redirect('employer_home')
    else:
        form = EmployerProfileForm()
    return render(request, 'Authorized/Core/Employer/create-employer-profile.html', {
        'form': form,
    })


# check this later might be wrong
@login_required()
@employer_required
def jobPostingPage(request):
    job  = get_object_or_404(Job, Job.job_uuid)
    return render(request, "Authorized/Employer/JobPostings_Employer.html")

@login_required
@employer_required
def candidatePage(request):
    return render(request, "Authorized/Employer/CandidateList.html")

@login_required
@employer_required
def profile(request):
    user = request.user
    profile = EmployerProfile.objects.get(user=user)
    return render(request,"Authorized/Employer/Profile_Employer.html", context={'profile' : profile})

@login_required
@employer_required
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

    return render(request, 'Authorized/Core/Employer/create-employer-profile.html', context={'form': form})
                
# @login_required
# def home(request):
#     if not request.user.has_completed_setup:
#         return redirect('setup')

@login_required
@employer_required
def employer_dashboard(request):
    return render(request, 'Authorized/Core/Employer/dashboard.html')
# make sure to grab dahsboard.html from karthik's branch

