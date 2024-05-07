from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

import Accounts.views
@login_required
def home(request):
    if not request.user.has_completed_setup:
        return redirect('setup')
    else:
        return redirect('dashboard')

@login_required()
def dashboard(request):
    return render(request, "Authorized/Core/dashboard.html")