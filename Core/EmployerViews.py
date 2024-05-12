import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from Core.EmployerForms import EditEmployerProfileForm, EmployerProfileForm, JobForm, EditJobForm
from Core.EmployerModel import EmployerProfile, Job, JobSkills
from Core.models import JobApplication
from ResumeAI.Generic.generic_decoraters import employer_required, emp_profile_completed, emp_profile_not_completed


@login_required
@employer_required
def emp_setupProfile(request):
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                profile, created = EmployerProfile.objects.get_or_create(user=request.user)
                profile.position = form.cleaned_data['position']
                profile.company_name = form.cleaned_data['company_name']
                profile.company_role_description = form.cleaned_data['company_role_description']
                profile.company_website = form.cleaned_data['company_website']
                profile.employer_completed = True
                profile.save()
            return redirect('home')
    else:
        form = EmployerProfileForm()
    return render(request, 'Authorized/Core/Employer/create-employer-profile.html', {
        'form': form,
    })


@login_required
@employer_required
@emp_profile_completed
def create_job_posting(request):
    employer_profile = EmployerProfile.objects.filter(user=request.user).first()
    if not employer_profile:
        messages.error(request, "Please complete your employer profile first.")
        return redirect('create_employer_profile')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            try:
                new_job = Job.objects.create(
                    employer_profile=employer_profile,
                    position=form.cleaned_data['position'],
                    description=form.cleaned_data['description'],
                    job_type=form.cleaned_data['job_type'],
                    pay=form.cleaned_data['pay'],
                    location=form.cleaned_data['location'],
                    link_to_apply=form.cleaned_data['link_to_apply']
                )
                skills_added = False
                skills = [form.cleaned_data.get(f'skill_{i}') for i in range(1, 6) if
                          form.cleaned_data.get(f'skill_{i}')]
                for skill_name in skills:
                    skill, created = JobSkills.objects.get_or_create(name=skill_name)
                    new_job.skills.add(skill)
                    skills_added = True
                if not skills_added:
                    messages.warning(request, "No skills were added to the job posting.")
                print("1: ", form.errors)
                messages.success(request, "Job posting created successfully.")
                return redirect('employer_dashboard')
            except Exception as e:
                messages.error(request, f"Failed to create job posting: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")
            print("2: ", form.errors)
    else:
        form = JobForm()
        print("3: ", form.errors)
    return render(request, 'Authorized/Core/Employer/create-job-posting.html', {
        'form': form,
        'profile': employer_profile  # Pass profile to handle it in the template
    })


@login_required
@employer_required
@emp_profile_completed
def edit_job_posting(request, job_uuid):
    job = get_object_or_404(Job, job_uuid=job_uuid)
    if request.method == 'POST':
        form = EditJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job posting updated successfully.")
            return redirect('job_posting_page')

        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EditJobForm(instance=job)

    return render(request, 'Authorized/Core/Employer/edit-job-posting.html', {'form': form, 'job': job})


@login_required
@employer_required
@emp_profile_completed
def employer_dashboard(request):
    employer_profile = EmployerProfile.objects.get(user=request.user)
    jobs = Job.objects.filter(employer_profile=employer_profile).order_by('-id')[:3]

    # Preparing data for the last three applicants for each job
    jobs_with_applicants = []
    total_applicants = 0  # Initialize total applicants count
    for job in jobs:
        applicants = list(job.list_of_applicants.all())[:3]  # Get the last three applicants for each job
        total_applicants += job.list_of_applicants.count()  # Sum up all applicants
        jobs_with_applicants.append((job, applicants))

    active_job_listings = Job.objects.filter(employer_profile=employer_profile).count()  # Count of active jobs

    context = {
        'employer_profile': employer_profile,
        'jobs_with_applicants': jobs_with_applicants,
        'total_applicants': total_applicants,
        'active_job_listings': active_job_listings,
    }
    return render(request, 'Authorized/Core/Employer/employer_dashboard.html', context)


@login_required
@employer_required
@emp_profile_completed
def edit_employer_profile(request):
    user = request.user
    profile, created = EmployerProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = EditEmployerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('employer_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EditEmployerProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'Authorized/Core/Employer/edit_employer_profile.html', context)


@login_required
@employer_required
@emp_profile_completed
def company_profile_page(request):
    return render(request, "Authorized/Core/Employer/company_profile_page.html")


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
        'employer_profile': employer_profile,
    }

    return render(request, 'Authorized/Core/Employer/CandidateList.html', context=context)

@login_required
@employer_required
@emp_profile_completed
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
    employer_profile = EmployerProfile.objects.filter(user=request.user).first()
    if not employer_profile:
        messages.error(request, "You must complete your employer profile.")
        return redirect('create_employer_profile')

    jobs = Job.objects.filter(employer_profile=employer_profile)
    jobs_json = custom_job_serializer(jobs)
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
    jobs = Job.objects.filter(employer_profile=profile)
    return render(request, "Authorized/Core/Employer/Profile_Employer.html", context={'profile': profile, 'jobs': jobs})

@login_required
@employer_required
@emp_profile_completed
def delete_job(request, job_uuid):
    if request.method == 'POST':
        job = get_object_or_404(Job, job_uuid=job_uuid, employer_profile__user=request.user)
        job.delete()
        messages.success(request, 'Job successfully deleted')
        return redirect('job_posting_page')
    else:
        messages.error(request, "Invalid request")
        return redirect('job_posting_page')
