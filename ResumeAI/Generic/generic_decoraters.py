from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse

from Core.EmployerModel import EmployerProfile
from Core.models import UserProfile


def job_searcher_required(view_func):
    """
    Decorator to restrict access to views based on user's role.
    Only allows users with the role 'job_searcher' to access the view.
    """

    def _wrapped_view(request, *args, **kwargs):
        if request.user.role != 'job_searcher':
            raise PermissionDenied("Access Forbidden: Only Job Searchers are allowed to access this page.")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def js_profile_completed(view_func):
    """
    Ensure that only employers with a completed profile can access certain views.
    """
    def wrapper(request, *args, **kwargs):
        user = request.user
        try:
            profile = UserProfile.objects.get(user=user)
            if profile.profile_completed:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('js_setup_profile')
        except UserProfile.DoesNotExist:
            return redirect('js_setup_profile')
    return wrapper


def js_profile_not_completed(view_func):
    """
    Ensure that employers without a completed profile are redirected to complete their profile.
    """

    def wrapper(request, *args, **kwargs):
        user = request.user
        try:
            profile = UserProfile.objects.get(user=user)
            if profile.profile_completed:
                return HttpResponseForbidden("Access Forbidden: Profile already completed.")
            else:
                return view_func(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
            return redirect('js_setup_profile')

    return wrapper


def employer_required(view_func):
    """
    Decorator to restrict access to views based on user's role
    Only allows users with the role job_searcher to access the view.
    
    Maybe add something for Employer view too? 
    """

    def _wrapped_view(request, *args, **kwargs):
        if request.user.role != 'employer':
            return HttpResponseForbidden("Access Forbidden: Only Employers are allowed to access this page.")
        return view_func(request, *args, **kwargs)

    return _wrapped_view

def emp_profile_completed(view_func):
    """
    Ensure that only employers with a completed profile can access certain views.
    """
    def wrapper(request, *args, **kwargs):
        user = request.user
        try:
            profile = EmployerProfile.objects.get(user=user)
            if profile.employer_completed:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('emp_setupProfile')
        except EmployerProfile.DoesNotExist:
            return redirect('emp_setupProfile')
    return wrapper


def emp_profile_not_completed(view_func):
    """
    Ensure that employers without a completed profile are redirected to complete their profile.
    """

    def wrapper(request, *args, **kwargs):
        if request.user.role != 'employer':
            return HttpResponseForbidden("Access Forbidden: Only Employers are allowed to access this page.")
        user = request.user
        try:
            profile = EmployerProfile.objects.get(user=user)
            if profile.employer_completed:
                return HttpResponseForbidden("Access Forbidden: Profile already completed.")
            else:
                if request.method == 'GET' or request.path != reverse('emp_setupProfile'):
                    return view_func(request, *args, **kwargs)
        except EmployerProfile.DoesNotExist:
            # Render the setup profile template or raise an exception
            return redirect('emp_setupProfile')

    return wrapper