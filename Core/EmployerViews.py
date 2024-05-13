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
    """
    View function for setting up an employer profile.

    Args:
        request (HttpRequest): HTTP request object.

    Returns:
        HttpResponse: redirects the user to the home page or renders the employer profile setup form
    """
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
    """
    View function for creating a new job posting

    Args:
        request (HttpRequest): HTTP request object.

    Returns:
        HttpResponse: renders the job posting creation form or redirects the user to the employer dashboard

    """
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
    """
    View function for editing a job posting.

    This view allows employers to edit the details of a job posting. It retrieves the job object based on the job_uuid
    provided in the URL. If the request method is POST, it validates the form data submitted for editing the job.
    If the form is valid, it saves the changes and redirects to the job posting page. If the form is not valid, it
    displays error messages. If the request method is GET, it renders the edit job posting form with pre-filled data.

    Args:
        request (HttpRequest): The HTTP request object.
        job_uuid (str): The UUID of the job to be edited.

    Returns:
        HttpResponse: The HTTP response containing the edit job posting form.

    """
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
    """
    View function for rendering the employer dashboard.

    Args:
        request (HttpRequest): HTTP request object.

    Returns:
        HttpResponse: renders the employer dashboard template w/ employer's profile info and the latest job postings w/ the last
            three applicants for each job.

    """
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
    """
    View function for editing an employer profile.

    This view allows employers to edit their profile information. It retrieves the employer profile object associated
    with the current user. If the request method is POST, it validates the form data submitted for editing the profile.
    If the form is valid, it saves the changes and redirects to the employer dashboard. If the form is not valid, it
    displays error messages. If the request method is GET, it renders the edit employer profile form with pre-filled data.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the edit employer profile form.

    """
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
    """
    View function for displaying candidates for a job posting.
    Args:
        request (HttpRequest): HTTP request object.
        job_id (int): The ID of the job posting.

    Returns:
        HttpResponse: renders the candidate list template with the candidates for the specified job posting

    """
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
    """
    View function to update the status of a candidate application for a job posting.

    This function allows an employer user to update the status of a candidate application for a specific job posting.
    It retrieves the job application object based on the provided application ID, validates the new status provided
    via a POST request, and updates the status accordingly. If the provided status is valid, it saves the changes and
    redirects to the candidate list page for the corresponding job posting. If the status is invalid or if the request
    method is not POST, it redirects to an appropriate error page.

    Args:
        request (HttpRequest): The HTTP request object.
        application_id (int): The ID of the job application to be updated.

    Returns:
        HttpResponseRedirect: Redirects to the candidate list page for the corresponding job posting if successful.
        HttpResponseRedirect: Redirects to an appropriate error page if the request method is not POST or if the
        provided status is invalid.
    """
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
    """
    Custom serializer function for serializing job objects into a JSON-compatible format.

    This function takes a queryset or list of job objects as input and serializes each job object into a dictionary
    format suitable for JSON serialization. It includes relevant fields and related data such as applicant count, company
    name, job position, job description, company role description, LinkedIn URL, job location, payment details, links to
    apply and company website, job type, and skills required.
    Used in job posting

    Args:
        jobs (QuerySet or list): Queryset or list of job objects to be serialized.

    Returns:
        list: A list of dictionaries, each representing a serialized job object.
    """
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
    """
    View function for displaying all job postings.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: renders the job postings template with the list of all job postings

    """
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
    """
    View function for displaying the employer profile.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: renders the employer profile template with the profile information.

    """
    user = request.user
    profile = EmployerProfile.objects.get(user=user)
    jobs = Job.objects.filter(employer_profile=profile)
    return render(request, "Authorized/Core/Employer/Profile_Employer.html", context={'profile': profile, 'jobs': jobs})

@login_required
@employer_required
@emp_profile_completed
def delete_job(request, job_uuid):
    """
    View function for deleting a job posting.

    This view allows employers to delete a job posting. It verifies that the request method is POST. If so, it retrieves
    the job object with the given UUID and associated with the current user as the employer. It then deletes the job
    object and redirects to the job posting page with a success message. If the request method is not POST, it displays
    an error message and redirects to the job posting page.

    Args:
        request (HttpRequest): The HTTP request object.
        job_uuid (str): The UUID of the job to be deleted.

    Returns:
        HttpResponse: The HTTP response redirecting to the job posting page with a success message or an error message.
    """
    if request.method == 'POST':
        job = get_object_or_404(Job, job_uuid=job_uuid, employer_profile__user=request.user)
        job.delete()
        messages.success(request, 'Job successfully deleted')
        return redirect('job_posting_page')
    else:
        messages.error(request, "Invalid request")
        return redirect('job_posting_page')
