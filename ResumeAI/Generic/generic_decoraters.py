<<<<<<< HEAD
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden

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

def js_profile_not_completed(view_func):
    """
    Decorator to restrict access to views based on user's profile being completed.
    Only allows users with the role 'job_searcher' to access the view.
    """
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.get(user=user)
        if profile.profile_completed:
            raise PermissionDenied("Access Forbidden: Can only access page if profile has not been completed")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def js_profile_completed(view_func):
    """
    Decorator to restrict access to views based on user's profile being completed.
    Only allows users with the role 'job_searcher' to access the view.
    """
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.get(user=user)
        if not profile.profile_completed:
            raise PermissionDenied("Access Forbidden: Can only access page if profile has not been completed")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
=======
from django.http import HttpResponseForbidden

def job_searcher_required(view_func):
    """
    Decorator to restrict access to views based on user's role
    Only allows users with the role job_searcher to access the view.
    
    Maybe add something for Employer view too? 
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role != 'job_searcher':
            return HttpResponseForbidden("Access Forbidden: Only Job Searchers are allowed to access this page.")
        return view_func(request, *args, *kwargs)
    return _wrapped_view

def employer_required(view_func):
    """
    Decorator to restrict access to views based on user's role
    Only allows users with the role job_searcher to access the view.
    
    Maybe add something for Employer view too? 
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role != 'employer':
            return HttpResponseForbidden("Access Forbidden: Only Employers are allowed to access this page.")
        return view_func(request, *args, *kwargs)
    return _wrapped_view
>>>>>>> Main/robert
