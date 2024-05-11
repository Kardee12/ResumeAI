from django.contrib.auth import logout
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from allauth.account.views import LoginView
from django.template import RequestContext

from Core.EmployerModel import EmployerProfile
from Core.models import UserProfile

def index(request):
    return render(request, "Unauthorized/Core/index.html")



@login_required
def home(request):
    user = request.user

    # Redirect if the user setup is not complete
    if not user.has_completed_setup:
        return redirect('setup')

    if user.role == 'job_searcher':
        try:
            UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return redirect('js_setup_profile')
        return redirect('jobsearcher_dashboard')
    else:  # Assuming the only other role is 'employer'
        try:
            EmployerProfile.objects.get(user=user)
        except EmployerProfile.DoesNotExist:
            return redirect('emp_setupProfile')
        return redirect('employer_dashboard')
@login_required
def settings(request):
    try:
        social_account = SocialAccount.objects.get(user=request.user)
    except SocialAccount.DoesNotExist:
        social_account = None

    if request.method == 'POST':
        if 'sign_out' in request.POST:
            logout(request)
            return redirect('/')
        elif 'delete_account' in request.POST:
            request.user.delete()
            return redirect('/')

    return render(request, 'Authorized/Core/JobSearcher/Settings.html', {
        'social_account': social_account,
    })

@login_required
def empsettings(request):
    try:
        social_account = SocialAccount.objects.get(user=request.user)
    except SocialAccount.DoesNotExist:
        social_account = None
    if request.method == 'POST':
        if 'sign_out' in request.POST:
            logout(request)
            return redirect('/')
        elif 'delete_account' in request.POST:
            request.user.delete()
            return redirect('/')

    return render(request, 'Authorized/Core/Employer/Settings.html', {
        'social_account': social_account    })


def logoutView(request):
    return render(request, 'Unauthorized/Accounts/logout.html')


def custom_logout(request):
    logout(request)
    return redirect('/logout')


class logView(LoginView):
    template_name = 'Unauthorized/Accounts/login.html'

def permission_denied(request, exception):
    context = {}
    return render(request, 'Authorized/Errors/403.html', context, status=403)