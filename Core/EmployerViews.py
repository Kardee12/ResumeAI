import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404

from Core.functions import ParsingUtility
from Core.functions.ParsingUtility import ParsingFunctions
from ResumeAI import settings
from ResumeAI.Generic.generic_decoraters import employer_required, emp_profile_completed, emp_profile_not_completed
from Core.EmployerForms import EmployerProfileForm, JobForm
from Core.EmployerModel import EmployerProfile, Job, JobSkills
from django.db import transaction, models
from django.db.models import Count, Q
from django.core import serializers


@login_required
@employer_required
@emp_profile_not_completed
def emp_setupProfile(request):
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                profile, created = EmployerProfile.objects.get_or_create(user = request.user)
                profile.position = form.cleaned_data['position']
                profile.company_name = form.cleaned_data['company_name']
                profile.company_description = form.cleaned_data['company_description']
                profile.company_website = form.cleaned_data['company_website']
                profile.employer_completed = True
                profile.save()
            return redirect('home')
    else:
        form = EmployerProfileForm()
    return render(request, 'Authorized/Core/Employer/create-employer-profile.html', {
        'form': form,
    })

# @login_required
# @employer_required
# def create_job_posting(request):
#     skills = ResumeSkills.objects.all()
#     skill_choices = [(skill.id, skill.name) for skill in skills]
    
#     if request.method == 'POST':
#         form = JobForm(request.POST, request.FILES)
#         form.fields['skills_used'].choices = skill_choices
#         if form.is_valid():
#             job = Job.objects.create(
#                 position=form.cleaned_data['position'],
#                 description=form.cleaned_data['description'],
#                 pay=form.cleaned_data['pay'],
#                 link_to_apply=form.cleaned_data['link_to_apply'],
#                 link_to_company=form.cleaned_data['link_to_company'],
#                 company_image_url=form.cleaned_data['company_image'],
#             )
            
#             skills_used = form.cleaned_data['skills_used']
#             for skill_id in skills_used:
#                 skill = ResumeSkills.objects.get(id = skill_id)
#                 job.skills_used.add(skill)
                
#                 pass
#         else:
#             form = JobForm()
#             form.fields['skills_used'].choices = skill_choices
            
#         return render(request, 'Authorized/Core/Employer/create-job-posting.html', {
#             'form' : form
#         })

@login_required
@employer_required
@emp_profile_completed
def create_job_posting(request):
    try:
        employer_profile = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        return redirect('create_employer_profile')
    if request.method == 'POST':
        # Extract data from the POST request
        position = request.POST.get('position')
        description = request.POST.get('description')
        job_type = request.POST.get('job_type')
        pay = request.POST.get('pay')
        location = request.POST.get('location')
        link_to_apply = request.POST.get('link_to_apply')
        new_job = Job(
            employer_profile=employer_profile,
            position=position,
            description=description,
            job_type=job_type,
            pay=pay,
            location=location,
            link_to_apply=link_to_apply
        )
        print(new_job.job_type)
        new_job.save()
        for i in range(1, 6):
            skill_name = request.POST.get(f'skill_{i}')
            if skill_name:
                skill, created = JobSkills.objects.get_or_create(name=skill_name)
                new_job.skills.add(skill)

        new_job.save()
        return redirect('employer_dashboard')
    else:
        return render(request, 'Authorized/Core/Employer/create-job-posting.html')

@login_required
@employer_required
@emp_profile_completed
def employer_dashboard(request):
    employer_profile = EmployerProfile.objects.get(user=request.user)
    jobs = Job.objects.filter(employer_profile=employer_profile).order_by('-id')[:3]
    # Preparing data for the last three applicants for each job
    jobs_with_applicants = []
    for job in jobs:
        applicants = list(job.list_of_applicants.all())[:3]  # Get the last three applicants for each job
        jobs_with_applicants.append((job, applicants))

    context = {
        'employer_profile': employer_profile,
        'jobs_with_applicants': jobs_with_applicants,
    }
    return render(request, 'Authorized/Core/Employer/employer_dashboard.html', context)


# work on this later 5/6/24
@login_required
@employer_required
@emp_profile_completed
def company_profile_page(request):
    return render(request, "Authorized/Core/Employer/company_profile_page.html")
# work on this later 5/6/24: Check notebook
@login_required
@employer_required
@emp_profile_completed
def edit_company_page(request):
    return render(request, 'Authorized/Core/Employer/edit_company_profile.html')

@login_required
@employer_required
@emp_profile_completed
def candidatePage(request, job_id):
    job = get_object_or_404(Job, job_id)
    required_skills = job.skills_used.all()
    applicants = job.list_of_applicants.annotate(matching_skills_count=Count('user__resumeskills', filter=models.Q(user__resumeskills__in=required_skills))).order_by('-matching_skills_count')

    return render(request, 'Authorized/Core/Employer/CandidateList.html', {'applicants': applicants, 'job': job})

def custom_job_serializer(jobs):
    job_list = []
    for job in jobs:
        job_info = {
            'job_uuid': str(job.job_uuid),
            'fields': {
                'applicant_count': job.applicant_count,
                'company': job.employer_profile.company_name,
                'position': job.position,
                'description': job.description,
                'location': job.location,
                'pay': job.pay,
                'link_to_apply': job.link_to_apply,
                'link_to_company': job.employer_profile.company_website,
                'job_type': job.job_type,
                'skills': [skill.name for skill in job.skills.all()]
            }
        }
        job_list.append(job_info)
    return job_list

@login_required
@employer_required
@emp_profile_completed
def job_posting_page(request):
    jobs = Job.objects.all()
    jobs_json = custom_job_serializer(jobs)  # Use your custom serializer here
    context = {
        'jobs': jobs,
        'jobs_json': json.dumps(jobs_json)
    }
    return render(request, "Authorized/Core/Employer/JobPostings_Employer.html", context)
@login_required
@employer_required
@emp_profile_completed
def candidatePage(request):
    return render(request, "Authorized/Core/Employer/CandidateList.html")

@login_required
@employer_required
@emp_profile_completed
def profile(request):
    user = request.user
    profile = EmployerProfile.objects.get(user=user)
    return render(request,"Authorized/Core/Employer/Profile_Employer.html", context={'profile' : profile})

@login_required
@employer_required
@emp_profile_not_completed
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

