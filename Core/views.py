from allauth.account.views import LoginView
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Core.EmployerModel import EmployerProfile
from Core.models import UserProfile


def index(request):
    return render(request, "Unauthorized/Core/index.html")


@login_required
def home(request):
    """
    View function for the home page.

    If the user setup is not complete, it redirects to the setup page.
    If the user role is 'job_searcher', it redirects to the job searcher dashboard or setup profile page if the profile is not complete.
    If the user role is 'employer', it redirects to the employer dashboard or setup profile page if the profile is not complete.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the appropriate page based on the user's role and setup status.
    """
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
    """
    View function for the settings page.

    Retrieves the user's social account information if available.
    Handles POST requests to sign out or delete the user account.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect or HttpResponse: Redirects to the home page after signing out or deleting the account.
            Renders the settings page with the social account information if available.
    """
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
        'social_account': social_account})


def logoutView(request):
    """
    Renders the logout page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the logout page template.
    """
    return render(request, 'Unauthorized/Accounts/logout.html')


def custom_logout(request):
    """
    Logs out the user and redirects to the logout page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the logout page.
    """
    logout(request)
    return redirect('/logout')


class logView(LoginView):
    """
    Custom login view class inheriting from LoginView.

    Attributes:
        template_name (str): Specifies the template used for rendering the login page.
    """
    template_name = 'Unauthorized/Accounts/login.html'


def permission_denied(request, exception):
    """
    Renders the permission denied page.

    Args:
        request (HttpRequest): The HTTP request object.
        exception (Exception): The exception object.

    Returns:
        HttpResponse: Renders the permission denied page template with a status code of 403.
    """
    context = {}
    return render(request, 'Authorized/Errors/403.html', context, status=403)
