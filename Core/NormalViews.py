from django.contrib.auth import logout
from django.shortcuts import render

from ResumeAI import settings


# Create your views here.

def index(request):
    return render(request, "Unauthorized/Core/index.html")
