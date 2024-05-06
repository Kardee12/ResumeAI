from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
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
                profile.position = form.cleaned_data['position']
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
            new_job.save()
            
            # Handle many-to-many relations after saving the job
            new_job.skills_used.set(form.cleaned_data['skills_used'])
            
            if 'company_image' in request.FILES:
                new_job.company_image_url = request.FILES['company_image']
                new_job.save()

            return redirect('employer_dashboard')  # Redirect to the employer dashboard or another appropriate page
    else:
        # Prepopulate the skills_used choices
        form = JobForm()
        form.fields['skills_used'].choices = [(skill.id, skill.name) for skill in ResumeSkills.objects.all()]

    return render(request, 'Authorized/Core/Employer/create_job_posting1.html', {'form': form})

    

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
    job  = get_object_or_404(Job)
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

