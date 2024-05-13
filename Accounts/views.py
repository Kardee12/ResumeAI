from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import SetupForm


@login_required
def setup_view(request):
    """
    View function for user setup.

    This view handles both GET and POST requests. In a GET request, it renders the setup form. In a POST request,
    it processes the form data and updates the user's role, LinkedIn URL, and setup completion status accordingly.

    Args:
        request: The HTTP request object.
    """
    if request.method == 'POST':
        form = SetupForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            request.user.role = form.cleaned_data['role']
            request.user.linkedin_url = form.cleaned_data['linkedin_url']
            request.user.has_completed_setup = True
            request.user.save()
            print("REDIRECT")
            print("request.user.role: ", request.user.role)
            if request.user.role == "job_searcher":
                print("DONE")
                return redirect('js_setup_profile')
            else:
                return redirect('emp_setupProfile')
        else:
            print(form.errors)
    else:
        form = SetupForm()
    return render(request, 'Authorized/Accounts/setup.html', {'form': form})
