from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from Core.functions import ParsingUtility
from Core.functions.ParsingUtility import ParsingFunctions
from ResumeAI import settings
from ResumeAI.Generic.generic_decoraters import employer_required, emp_profile_completed, emp_profile_not_completed
from Core.EmployerForms import EmployerProfileForm, JobForm
from Core.EmployerModel import EmployerProfile, Job, JobSkills
from django.db import transaction, models
from django.db.models import Count


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
        # Handling manual fields like link to company and skills
        link_to_company = request.POST.get('link_to_company')
        skills = [request.POST.get(f'skill_{i}') for i in range(1, 11)]  # Adjust the range as needed
        aiParser = ParsingFunctions()
        normalized_skills = aiParser.normalize_skills([skill for skill in skills if skill])  # Normalize and filter out empty
        new_job = Job(
            employer_profile=employer_profile,
            position=request.POST.get('position'),
            description=request.POST.get('description'),
            job_type=request.POST.get('job_type'),
            pay=request.POST.get('pay'),
            location=request.POST.get('location'),
            link_to_apply=request.POST.get('link_to_apply'),
            link_to_company=request.POST.get('link_to_company'),
        )
        new_job.save()

        for skill_name in normalized_skills:
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

@login_required
@employer_required
@emp_profile_completed
def job_posting_page(request):

    jobs = Job.objects.all()
    return render(request, "Authorized/Core/Employer/JobPostings_Employer.html", {'jobs': jobs})


@login_required
@employer_required
@emp_profile_completed
def candidatePage(request, job_id):
    job = get_object_or_404(Job, job_id)
    required_skills = job.skills_used.all()
    applicants = job.list_of_applicants.annotate(matching_skills_count=Count('user__resumeskills', filter=models.Q(user__resumeskills__in=required_skills))).order_by('-matching_skills_count')

    return render(request, 'Authorized/Core/Employer/CandidateList.html', {'applicants': applicants, 'job': job})
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


    return render(request, 'Authorized/Core/Employer/dashboard.html')
