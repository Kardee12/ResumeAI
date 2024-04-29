from django.shortcuts import render

def employer_dashboard(request):
    return render(request, 'Authorized/Core/Employer/dashboard.html')