from django.contrib.auth import logout
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from allauth.account.views import LoginView

from Core.models import UserProfile


def index(request):
    return render(request, "Unauthorized/Core/index.html")


@login_required
def home(request):
    if not request.user.has_completed_setup:
        return redirect('setup')
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return redirect('js_setup_profile1')
    if request.user.role == 'job_searcher':
        return redirect('jobsearcher_dashboard')
    else:
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

    return render(request, 'Authorized/Core/Settings.html', {
        'social_account': social_account
    })

def logoutView(request):
    return render(request, 'Unauthorized/Accounts/logout.html')

def custom_logout(request):
    logout(request)
    return redirect('/logout')

class logView(LoginView):
    template_name = 'Unauthorized/Accounts/login.html'