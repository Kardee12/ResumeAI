from django.http import FileResponse, Http404
from Core.models import UserResume


def download_resume(request):
    try:
        user = request.user
        user_resume = UserResume.objects.get(user=user)
        filename = user_resume.resume.path
        response = FileResponse(open(filename, 'rb'))
        return response
    except UserResume.DoesNotExist:
        raise Http404("No resume found for this user.")
