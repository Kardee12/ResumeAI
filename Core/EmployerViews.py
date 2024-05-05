from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from Core import EmployerModel
from ResumeAI import settings
from ResumeAI.Generic.generic_decoraters import employer_required
from Core.EmployerForms import EmployerProfileForm, JobForm
from Core.EmployerModel import EmployerProfile, Job, ResumeSkills
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
            return redirect('employer_dashboard')
    else:
        form = EmployerProfileForm()
    return render(request, 'Authorized/Core/Employer/create-employer-profile.html', {
        'form': form,
    })

@login_required
@employer_required
def create_job_posting(request):
    skills = ResumeSkills.objects.all()
    skill_choices = [(skill.id, skill.name) for skill in skills]
    
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        form.fields['skills_used'].choices = skill_choices
        if form.is_valid():
            job = Job.objects.create(
                position=form.cleaned_data['position'],
                description=form.cleaned_data['description'],
                pay=form.cleaned_data['pay'],
                link_to_apply=form.cleaned_data['link_to_apply'],
                link_to_company=form.cleaned_data['link_to_company'],
                company_image_url=form.cleaned_data['company_image'],
            )
            
            skills_used = form.cleaned_data['skills_used']
            for skill_id in skills_used:
                skill = ResumeSkills.objects.get(id = skill_id)
                job.skills_used.add(skill)
                
                pass
        else:
            form = JobForm()
            form.fields['skills_used'].choices = skill_choices
        
        context = {
            'form' : form,
        }
        return render(request, 'Authorized/Core/Employer/create-job-posting.html', context)
    
# @login_required
# @employer_required
# def employer_dashboard(request):
#     try:
#         employer_profile = EmployerProfile.objects.get(user=request.user)
#     except EmployerProfile.DoesNotExist:
#         return redirect('emp_setupProfile')
#     return render(request, "Authorized/Employer/employer_dashboard.html", context={'profile' : profile})
    
# @login_required
# def employer_dashboard(request):
#     employer_profile = get_object_or_404(EmployerProfile, user=request.user)

#     # Get recent job postings
#     recent_jobs = employer_profile.job_set.order_by('-id')[:3]

#     # Get recent applicants
#     recent_applicants = []
#     for job in recent_jobs:
#         applicants = job.list_of_applicants.all().order_by('-id')[:3]
#         recent_applicants.extend(applicants)

#     # Calculate total applicants and active job postings
#     total_applicants = employer_profile.job_set.aggregate(total=EmployerModel.Sum('applicant_count'))['total'] or 0
#     active_job_postings = employer_profile.job_set.count()

#     # Retrieve available skills for the job form
#     skills = ResumeSkills.objects.all()
#     skill_choices = [(skill.id, skill.name) for skill in skills]

#     # Create an instance of the job form
#     job_form = JobForm()
#     job_form.fields['skills_used'].choices = skill_choices

#     context = {
#         'employer_profile': employer_profile,
#         'recent_jobs': recent_jobs,
#         'recent_applicants': recent_applicants,
#         'total_applicants': total_applicants,
#         'active_job_postings': active_job_postings,
#         'job_form': job_form,
#     }

#     return render(request, 'Authorized/Employer/employer_dashboard.html', context)

@login_required
@employer_required
def employer_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('index')  # Redirect to login if user is not authenticated

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


# check this later might be wrong
@login_required()
@employer_required
def jobPostingPage(request):
    job  = get_object_or_404(Job, Job.job_uuid)
    return render(request, "Authorized/Core/Employer/JobPostings_Employer.html")

@login_required
@employer_required
def candidatePage(request):
    return render(request, "Authorized/Core/Employer/CandidateList.html")

@login_required
@employer_required
def profile(request):
    user = request.user
    profile = EmployerProfile.objects.get(user=user)
    return render(request,"Authorized/Core/Employer/Profile_Employer.html", context={'profile' : profile})

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

# @login_required
# @employer_required
# def employer_dashboard(request):
#     return render(request, 'Authorized/Core/Employer/dashboard.html')
# # make sure to grab dahsboard.html from karthik's branch

