import os
from django.contrib.auth import logout
from django.db import transaction
from django.shortcuts import render, redirect

from Core.models import UserProfile, UserResume
from ResumeAI.Generic.generic_decoraters import job_searcher_required
from django.contrib.auth.decorators import login_required
from ResumeAI import settings
from .forms import UserProfileForm
from .functions.JobSearcherDBUtility import update_user_skills
from .functions.ParsingUtility import ResumeParsing, ParsingFunctions


@login_required
@job_searcher_required
def jobsearcher_dashboard(request):
    return render(request, 'Authorized/Core/JobSearcher/dashboard.html')


@login_required
@job_searcher_required
def jobsearcher_chat(request):
    return render(request, "Authorized/Core/JobSearcher/chat.html")


@login_required
@job_searcher_required
def jobsearcher_profile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    skills = ["Java", "Javascript", "AI","Python","Django"]
    return render(request, "Authorized/Core/JobSearcher/profile.html", context={
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'profile': profile,
        'skills' : skills,
    })


@login_required
def js_setup_profile(request):
    rparser = ResumeParsing(request)
    aiParser = ParsingFunctions()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                profile, created = UserProfile.objects.get_or_create(user=request.user)
                profile.location = form.cleaned_data['location']
                profile.bio = form.cleaned_data['bio']
                profile.profile_completed = True
                if 'resume' in request.FILES:
                    resume = UserResume.objects.create(
                        user=request.user,
                        resume=request.FILES['resume'],
                    )
                user_resume = UserResume.objects.get(user=request.user)
                extracted_text = None
                skills = None
                if user_resume and user_resume.resume:
                    if user_resume.resume.name.endswith('.pdf'):
                        extracted_text = rparser.extract_text_from_pdf()
                    elif user_resume.resume.name.endswith('.docx'):
                        extracted_text = rparser.extract_text_from_docx()
                    elif user_resume.resume.name.endswith('.doc'):
                        extracted_text = rparser.extract_text_from_doc()
                if extracted_text:
                    output = aiParser.gen_query(extracted_text)
                    skills = aiParser.post_processing(output)
                    if skills:
                        update_user_skills(request.user, skills)
                else:
                    print("ERROR: Unable to parse the resume or no skills extracted.")
                profile.resume = resume
                profile.save()
                print(str(profile))
            return redirect('home')
    else:
        form = UserProfileForm()
    return render(request, 'Authorized/Core/JobSearcher/create-profile.html',
                  {'form': form,
                   'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY})


@login_required
def edit_profile(request):
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
            profile.save()
        return redirect('jobsearcher_profile')

    context = {
        'profile': profile,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'Authorized/Core/JobSearcher/edit-profile.html', context)