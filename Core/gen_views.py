from django.http import FileResponse, Http404
<<<<<<< HEAD
from Core.models import UserResume

=======

from Core.models import UserResume
>>>>>>> origin/Karthik

def download_resume(request):
    try:
        user = request.user
        user_resume = UserResume.objects.get(user=user)
        filename = user_resume.resume.path
        response = FileResponse(open(filename, 'rb'))
        return response
    except UserResume.DoesNotExist:
<<<<<<< HEAD
        raise Http404("No resume found for this user.")
=======
        raise Http404("No resume found for this user.")
>>>>>>> origin/Karthik
