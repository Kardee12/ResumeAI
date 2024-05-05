from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SetupForm

@login_required
def setup_view(request):
    if request.method == 'POST':
        form = SetupForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            request.user.role = form.cleaned_data['role']
            request.user.linkedin_url = form.cleaned_data['linkedin_url']
            request.user.has_completed_setup = True
            request.user.save()
            print("REDIRECT")
            if request.user.role == "job_searcher":
                return redirect('js_setup_profile')
            else:
                return redirect('emp_setupProfile')
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = SetupForm()
    return render(request, 'Authorized/Accounts/setup.html', {'form': form})