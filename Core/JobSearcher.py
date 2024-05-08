import io
import json
import os
from datetime import timedelta, datetime

from django.contrib import messages
from django.core import serializers
from django.core.files.base import ContentFile
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST

from Core.models import UserProfile, UserResume, UserSkill, JobApplication
from ResumeAI.Generic.generic_decoraters import job_searcher_required, js_profile_completed, js_profile_not_completed
from django.contrib.auth.decorators import login_required
from ResumeAI import settings
from . import models
from .EmployerModel import Job
from .forms import UserProfileForm, ResumeForm
from .functions.ChatUtility import query_model
from .functions.GenerationUtility import generate_resume_text
from .functions.JobSearcherDBUtility import create_user_skills, update_user_skills
from .functions.ParsingUtility import ResumeParsing, ParsingFunctions

from django.db import transaction
from django.db.models import Q, Count


@login_required
@job_searcher_required
@js_profile_completed
def jobsearcher_dashboard(request):
    user = request.user
    today = datetime.today()
    last_month = today - timedelta(days=30)

    total_applications = JobApplication.objects.filter(user=user).count()
    total_open_applications = JobApplication.objects.filter(user=user, status='applied').count()
    total_interviews = JobApplication.objects.filter(user=user, status='interview').count()
    total_offers = JobApplication.objects.filter(user=user, status='offer').count()
    total_rejections = JobApplication.objects.filter(user=user, status='rejected').count()
    last_month_applications = JobApplication.objects.filter(user=user, application_date__lt=last_month).count()
    last_month_open_applications = JobApplication.objects.filter(user=user, status='applied', application_date__lt=last_month).count()
    last_month_interviews = JobApplication.objects.filter(user=user, status='interview', application_date__lt=last_month).count()
    last_month_offers = JobApplication.objects.filter(user=user, status='offer', application_date__lt=last_month).count()
    last_month_rejections = JobApplication.objects.filter(user=user, status='rejected', application_date__lt=last_month).count()
    change_applications = total_applications - last_month_applications
    change_open_applications = total_open_applications - last_month_open_applications
    change_interviews = total_interviews - last_month_interviews
    change_offers = total_offers - last_month_offers
    change_rejections = total_rejections - last_month_rejections
    success_rate = float (float(total_offers) / float(total_applications)) if (total_applications and total_offers) > 0 else 0
    context = {
        'job_applications': JobApplication.objects.filter(user=user).order_by('-application_date')[:3],
        'total_applications': total_applications,
        'total_open_applications': total_open_applications,
        'total_interviews': total_interviews,
        'total_offers': total_offers,
        'total_rejections': total_rejections,
        'change_applications': change_applications,
        'change_open_applications': change_open_applications,
        'change_interviews': change_interviews,
        'change_offers': change_offers,
        'change_rejections': change_rejections,
        'success_rate': success_rate,
    }
    return render(request, 'Authorized/Core/JobSearcher/dashboard.html', context)


@login_required
@job_searcher_required
@js_profile_completed
def jobsearcher_profile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    skills = profile.skills.all()[:6]
    print(skills)
    return render(request, "Authorized/Core/JobSearcher/profile.html", context={
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'profile': profile,
        'skills': skills
    })

@login_required
@job_searcher_required
@js_profile_completed
def update_skills(request):
    if request.method == 'POST':
        user = request.user
        profile = UserProfile.objects.get(user=user)
        skills_names = request.POST.getlist('skills')
        profile.skills.clear()
        for name in skills_names:
            skill, created = UserSkill.objects.get_or_create(name=name)
            profile.skills.add(skill)
        profile.save()

        return redirect('jobsearcher_profile')
    return redirect('jobsearcher_dashboard')


@login_required
@job_searcher_required
@js_profile_not_completed
def js_setup_profile(request):
    rparser = ResumeParsing(request)
    aiParser = ParsingFunctions()
    resume_error = None
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                profile, created = UserProfile.objects.get_or_create(user=request.user)
                profile.location = form.cleaned_data['location']
                profile.bio = form.cleaned_data['bio']
                if 'resume' in request.FILES:
                    resume = UserResume.objects.create(
                        user=request.user,
                        resume=request.FILES['resume']
                    )
                    profile.resume = resume
                user_resume = UserResume.objects.get(user=request.user)
                extracted_text = None
                if user_resume and user_resume.resume:
                    if user_resume.resume.name.endswith('.pdf'):
                        extracted_text = rparser.extract_text_from_pdf()
                    elif user_resume.resume.name.endswith('.docx'):
                        extracted_text = rparser.extract_text_from_docx()
                    elif user_resume.resume.name.endswith('.doc'):
                        extracted_text = rparser.extract_text_from_doc()
                if extracted_text:
                    output = aiParser.gen_query(extracted_text)
                    top_skills = aiParser.post_processing(output)
                    if len(top_skills) > 4:
                        create_user_skills(request.user, top_skills)
                    else:
                        resume_error = "No skills extracted, parsing error, or we want more information."
                else:
                    resume_error = "Unable to parse the resume."
                profile.save()
                if resume_error:
                    messages.error(request, resume_error)
                    return redirect('create-resume')
                profile.profile_completed = True
                profile.save()
            return redirect('home')
        else:
            messages.error(request, "Form validation failed.")
    else:
        form = UserProfileForm()
    return render(request, 'Authorized/Core/JobSearcher/create-profile.html', {
        'form': form,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    })

@login_required
@job_searcher_required
@js_profile_completed
def edit_profile(request):
    rparser = ResumeParsing(request)
    aiParser = ParsingFunctions()
    resume_error = None
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if request.method == 'POST':
        location = request.POST.get('location')
        bio = request.POST.get('summary')
        resume_file = request.FILES.get('resume')
        with transaction.atomic():
            if profile is None:
                profile = UserProfile.objects.create(user=request.user)
            if location and location != profile.location:
                profile.location = location
            if bio and bio != profile.bio:
                profile.bio = bio
            skills_extracted = False
            if resume_file:
                new_resume = UserResume(
                    user=request.user,
                    resume=resume_file
                )
                new_resume.save()
                extracted_text = None
                if new_resume.resume.name.endswith('.pdf'):
                    extracted_text = rparser.extract_text_from_pdf()
                elif new_resume.resume.name.endswith('.docx'):
                    extracted_text = rparser.extract_text_from_docx()
                elif new_resume.resume.name.endswith('.doc'):
                    extracted_text = rparser.extract_text_from_doc()
                elif new_resume.resume.name.endswith('.txt'):
                    extracted_text = rparser.extract_text_from_txt()
                if extracted_text:
                    output = aiParser.gen_query(extracted_text)
                    skills = aiParser.post_processing(output)
                    if len(skills) >= 4:
                        skills_extracted = True
                        if profile.resume:
                            old_resume = profile.resume
                            if old_resume.resume and os.path.isfile(old_resume.resume.path):
                                os.remove(old_resume.resume.path)
                            old_resume.delete()
                        profile.resume = new_resume
                        update_user_skills(request.user, skills)
                    else:
                        new_resume.delete()
                        resume_error = "Insufficient number of skills extracted from resume."
                else:
                    new_resume.delete()
                    resume_error = "Unable to parse the resume."

            if not resume_file or (resume_file and skills_extracted):
                profile.save()
        if resume_error:
            messages.error(request, resume_error)
            return redirect('jobsearcher_profile')

        return redirect('jobsearcher_profile')

    context = {
        'profile': profile,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'Authorized/Core/JobSearcher/edit-profile.html', context)


@login_required
@job_searcher_required
@js_profile_not_completed
def create_resume(request):
    form = ResumeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            profile, created = UserProfile.objects.get(user=request.user)
            resume_text = generate_resume_text(request.user, form.cleaned_data)
            resume_file = io.BytesIO(resume_text.encode())
            file_name = f"{request.user.username}_resume.txt"
            resume, created = UserResume.objects.update_or_create(
                user=request.user,
                defaults={'resume': ContentFile(resume_file.read(), name=file_name)}
            )
            profile.resume = resume
            skills = []
            for i in range(1, 11):
                skill_name = form.cleaned_data.get(f'skill_{i}')
                if skill_name:
                    skill, _ = UserSkill.objects.get_or_create(name=skill_name)
                    skills.append(skill)
            profile.skills.set(skills)
            profile.profile_completed = True
            profile.save()
            return redirect('home')
    else:
        form = ResumeForm()
    return render(request, 'Authorized/Core/JobSearcher/create-resume.html', {'form': form})


@login_required
@job_searcher_required
@js_profile_completed
def jobsearcher_chat(request):
    return render(request, "Authorized/Core/JobSearcher/chat.html")

@never_cache
@csrf_exempt
@login_required
@js_profile_completed
@require_http_methods(["POST"])
def processMessages(request):
    message = request.POST.get('message', '')
    if not message:
        return JsonResponse({'error': 'No message provided'}, status=400)
    user_profile = UserProfile.objects.filter(user=request.user).first()
    if not user_profile or not user_profile.resume:
        return JsonResponse({'error': 'No resume available'}, status=404)
    resume = user_profile.resume
    extracted_text = ""
    rparser = ResumeParsing(request)
    if resume.resume.name.endswith('.pdf'):
        extracted_text = rparser.extract_text_from_pdf()
    elif resume.resume.name.endswith('.docx'):
        extracted_text = rparser.extract_text_from_docx()
    elif resume.resume.name.endswith('.doc'):
        extracted_text = rparser.extract_text_from_doc()
    elif resume.resume.name.endswith('.txt'):
        extracted_text = rparser.extract_text_from_txt()
    response = query_model(message, extracted_text)
    print(response)
    return JsonResponse({'api_response': response['answer']})

@never_cache
@csrf_exempt
@js_profile_completed
@login_required
def clearChat(request):
    if 'conversation_memory' in request.session:
        del request.session['conversation_memory']
    return JsonResponse({'success': True}, status=200)


def custom_job_serializer(jobs):
    job_list = []
    for job in jobs:
        job_info = {
            'pk': job.pk,
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

@csrf_exempt
@js_profile_completed
@login_required
def search(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_skill_names = user_profile.skills.values_list('name', flat=True)
    query = request.GET.get('q', '')
    if query:
        jobs = Job.objects.filter(
            Q(position__icontains=query) | Q(description__icontains=query) |
            Q(company__icontains=query) | Q(location__icontains=query) |
            Q(pay__icontains=query) | Q(job_type__icontains=query)
        ).distinct()
    else:
        jobs = Job.objects.all()
        jobs = jobs.prefetch_related('skills')
        jobs = jobs.filter(skills__name__in=user_skill_names).distinct() if user_skill_names else jobs
    print(jobs)
    jobs_data = custom_job_serializer(jobs)
    jobs_json = json.dumps(jobs_data)
    return render(request, 'Authorized/Core/JobSearcher/searcher.html', {'jobs_json': jobs_json, 'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY})


@require_POST
@login_required
def apply_for_job(request):
    job_id = request.GET.get('job_id')
    user = request.user

    try:
        job = Job.objects.get(pk=job_id)
        with transaction.atomic():
            application, created = JobApplication.objects.get_or_create(user=user, job=job)
            if created:
                application.status = 'applied'
                application.save()
                job.applicant_count += 1
                job.list_of_applicants.add(user)
                print(job.list_of_applicants)
                job.save()
                print(f"Application created for user {user.username} to job {job.position}")
            else:
                print(f"Application already exists for user {user.username} to job {job.position}")

        return JsonResponse({"success": True}, status=200)
    except Job.DoesNotExist:
        print(f"Job with id {job_id} not found")
        return JsonResponse({"success": False, "error": "Job not found"}, status=404)
    except Exception as e:
        print(f"Error applying for job: {str(e)}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
@js_profile_completed
@login_required
def all_job_apps(request):
    user = request.user
    job_applications = JobApplication.objects.filter(user=user).order_by('-application_date')
    context = {
        'job_applications': job_applications,
    }
    return render(request, 'Authorized/Core/JobSearcher/all_job_applications.html', context)