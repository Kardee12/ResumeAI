from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from ResumeAI import settings
from ResumeAI.Generic.generic_decoraters import employer_required
from Core.EmployerForms import EmployerProfileForm
from Core.EmployerModel import EmployerProfile, Job
from django.db import transaction, models
from django.db.models import Count
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
@login_required
@employer_required
def jobPostingPage(request):
    jobs = Job.objects.all()
    return render(request, "Authorized/Core/Employer/JobPostings_Employer.html", {'jobs': jobs})


@login_required
@employer_required
def candidatePage(request, job_id):
    job = get_object_or_404(Job, job_id)
    required_skills = job.skills_used.all()
    applicants = job.list_of_applicants.annotate(matching_skills_count=Count('user__resumeskills', filter=models.Q(user__resumeskills__in=required_skills))).order_by('-matching_skills_count')

    return render(request, 'Authorized/Core/Employer/CandidateList.html', {'applicants': applicants, 'job': job})
@login_required
@employer_required
def profile(request):
    user = request.user
    profile = EmployerProfile.objects.get(user=user)
    return render(request,"'Authorized/Core/Employer/Profile_Employer.html", context={'profile' : profile})

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