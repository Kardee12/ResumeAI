import io
import os

from django.contrib import messages
from django.core.files.base import ContentFile
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from Core.models import UserProfile, UserResume, UserSkill
from ResumeAI.Generic.generic_decoraters import job_searcher_required, js_profile_completed, js_profile_not_completed
from django.contrib.auth.decorators import login_required
from ResumeAI import settings
from .forms import UserProfileForm, ResumeForm
from .functions.GenerationUtility import generate_resume_text
from .functions.JobSearcherDBUtility import create_user_skills, update_user_skills
from .functions.ParsingUtility import ResumeParsing, ParsingFunctions


@login_required
@job_searcher_required
@js_profile_completed
def jobsearcher_dashboard(request):
    return render(request, 'Authorized/Core/JobSearcher/dashboard.html')

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
            if resume_file:
                if profile.resume:
                    old_resume = profile.resume
                    if old_resume.resume and os.path.isfile(old_resume.resume.path):
                        os.remove(old_resume.resume.path)
                    old_resume.delete()
                new_resume = UserResume(
                    user=request.user,
                    resume=resume_file
                )
                new_resume.save()
                profile.resume = new_resume
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
                    if skills:
                        update_user_skills(request.user, skills)

            profile.save()
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
            resume_text = generate_resume_text(request.user,form.cleaned_data)
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


def query_model(question, context):
    return "Simulated response based on your resume and question: " + question
@never_cache
@csrf_exempt
@login_required
@require_http_methods(["POST"])
@login_required
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
    return JsonResponse({'api_response': response})