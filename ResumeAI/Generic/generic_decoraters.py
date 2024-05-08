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
        return view_func(request, *args, **kwargs)
    return _wrapped_view