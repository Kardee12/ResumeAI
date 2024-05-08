from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from ResumeAI import settings
from ResumeAI.Generic.generic_decoraters import employer_required, emp_profile_completed, emp_profile_not_completed
from Core.EmployerForms import EmployerProfileForm, JobForm
from Core.EmployerModel import EmployerProfile, Job, ResumeSkills
from django.db import transaction, models
from django.db.models import Count
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
    employer_profile = EmployerProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new job instance, without saving to the DB yet
            new_job = Job(
                employer_profile=employer_profile,
                position=form.cleaned_data['position'],
                description=form.cleaned_data['description'],
                pay=form.cleaned_data['pay'],
                link_to_apply=form.cleaned_data['link_to_apply'],
                link_to_company=form.cleaned_data['link_to_company'],
            )

            employer_profile.save()
            new_job.save()
            new_job.skills_used.set(form.cleaned_data['skills_used'])
            
            if 'company_image' in request.FILES:
                new_job.company_image_url = request.FILES['company_image']
                new_job.save()

            return redirect('employer_dashboard')
    else:
        form = JobForm()
        form.fields['skills_used'].choices = [(skill.id, skill.name) for skill in ResumeSkills.objects.all()]

    return render(request, 'Authorized/Core/Employer/create_job_posting1.html', {'form': form})

@login_required
@employer_required
def edit_job_posting(request, job_id):
    job = get_object_or_404(Job, job_uuid=job_id)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_posting_page')  # Redirect to the job posting overview page
    else:
        form = JobForm(instance=job)

    return render(request, 'edit_job_posting.html', {'form': form, 'job': job})
    

@login_required
@employer_required
@emp_profile_completed
def employer_dashboard(request):
    employer_profile = EmployerProfile.objects.get(user=request.user)
    jobs = Job.objects.filter(employer_profile=employer_profile).order_by('-id')[:3]
    total_job_postings = Job.objects.filter(employer_profile=employer_profile).count()

    # Preparing data for the last three applicants for each job
    jobs_with_applicants = []
    for job in jobs:
        applicants = list(job.list_of_applicants.all())[:3]  # Get the last three applicants for each job
        jobs_with_applicants.append((job, applicants))

    context = {
        'employer_profile': employer_profile,
        'jobs_with_applicants': jobs_with_applicants,
        'total_job_postings' : total_job_postings,
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
    job = get_object_or_404(Job, job_uuid=job_id)  # Use the correct field name here
    required_skills = job.skills_used.all()
    applicants = job.list_of_applicants.annotate(
        matching_skills_count=Count(
            'user__resumeskills',
            filter=models.Q(user__resumeskills__in=required_skills)
        )
    ).order_by('-matching_skills_count')

    return render(request, 'Authorized/Core/Employer/CandidateList.html', {'applicants': applicants, 'job': job})

@login_required
@employer_required
@emp_profile_completed
def job_posting_page(request):
    jobs = Job.objects.all()
    jobs_json = serializers.serialize('json', jobs, fields=('job_uuid', 'position', 'description', 'company_image_url', 'link_to_apply', 'company_domain'))
    default_image_url = 'https://example.com/default-image.jpg'  # Provide a default image URL
    return render(request, "authorized/core/employer/jobpostings_employer.html", {
        'jobs': jobs,
        'jobs_json': jobs_json,
        'default_image_url': default_image_url
    })

@login_required
@employer_required
@emp_profile_completed
def candidatePage(request, job_id):  # 'job_id' is correctly expected here
    # Make sure the field in get_object_or_404 matches your model's field
    job = get_object_or_404(Job, job_uuid=job_id)
    return render(request, 'Authorized/Core/Employer/CandidateList.html', {'job': job})

@login_required
@employer_required
@emp_profile_completed
def profile(request):
    user = request.user
    employer_profile = EmployerProfile.objects.get(user=request.user)
    jobs = Job.objects.filter(employer_profile=employer_profile).order_by('-id')[:3]
    profile = EmployerProfile.objects.get(user=user)
    context = {
        'profile' : profile,
        'jobs' : jobs
    }
    return render(request,"Authorized/Core/Employer/Profile_Employer.html", context)

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

