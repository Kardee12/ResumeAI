import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from Core.functions import ParsingUtility
from Core.functions.ParsingUtility import ParsingFunctions
from Core.models import JobApplication
from ResumeAI import settings
from ResumeAI.Generic.generic_decoraters import employer_required, emp_profile_completed, emp_profile_not_completed
from Core.EmployerForms import EditEmployerProfile, EmployerProfileForm, JobForm
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
def edit_job_posting(request, job_id):
    job = get_object_or_404(Job, job_uuid=job_id)
    if request.method == 'POST':
        position = request.POST.get('position')
        description = request.POST.get('description')
        job_type = request.POST.get('job_type')
        pay = request.POST.get('pay')
        location = request.POST.get('location')
        link_to_apply = request.POST.get('link_to_apply')
        if position and position != job.position:
            job.position = position
        if description and description != job.description:
            job.description = description
        if job_type and job_type != job.job_type:
            job.job_type = job_type
        if pay and pay != job.pay:
            job.pay = pay
        if location and location != job.location:
            job.location = location
        if link_to_apply and link_to_apply != job.link_to_apply:
            job.link_to_apply = link_to_apply
        current_skills = {skill.name for skill in job.skills.all()}
        new_skills = set(request.POST.get(f'skill_{i}') for i in range(1, 6) if request.POST.get(f'skill_{i}'))
        if new_skills != current_skills:
            job.skills.clear()
            for skill_name in new_skills:
                if skill_name:
                    skill, created = JobSkills.objects.get_or_create(name=skill_name)
                    job.skills.add(skill)

        job.save()
        return redirect('job_posting_page')
    else:
        context = {
            'job': job,
            'skills': job.skills.all()
        }
        return render(request, 'Authorized/Core/Employer/edit-job-posting.html', context)

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

@login_required
@employer_required
@emp_profile_completed
def edit_employer_profile(request):
    user = request.user
    profile, created = EmployerProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        position = request.POST.get('position')
        company_description = request.POST.get('company_description')
        company_website = request.POST.get('company_website')

        with transaction.atomic():
            if position and position != profile.position:
                profile.position = position
            if company_description and company_description != profile.company_description:
                profile.company_description = company_description
            if company_website and company_website != profile.company_website:
                profile.company_website = company_website

            profile.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('employer_dashboard')

    context = {
        'profile': profile
    }
    return render(request, 'Authorized/Core/Employer/edit_employer_profile.html', context)


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
    job = get_object_or_404(Job, job_uuid=job_id)
    job_applications = JobApplication.objects.filter(job=job)
    employer_profile = EmployerProfile.objects.get(user=request.user)
    candidates = [app.user.profile for app in job_applications if app.user.profile.profile_completed]

    context = {
        'job': job,
        'candidates': candidates,
        'employer_profile' : employer_profile,
    }

    return render(request, 'Authorized/Core/Employer/CandidateList.html', context = context)

def update_candidate_status(request, application_id):
    job_application = get_object_or_404(JobApplication, id=application_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(JobApplication.STATUS_CHOICES):
            job_application.status = new_status
            job_application.save()
            return redirect('candidate_list', job_id=job_application.job.job_uuid)
        else:
            return redirect('job_posting_page')

    return redirect('some_error_page')  # Redirect somewhere appropriate if not a POST request
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
                'company_role_description': job.employer_profile.company_role_description,
                'linkedin': job.employer_profile.user.linkedin_url,
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

