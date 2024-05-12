import uuid

from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404

from Core.models import UserResume
from ResumeAI.Generic.generic_decoraters import emp_profile_completed, employer_required


def download_resume(request):
    try:
        user = request.user
        user_resume = user.resumes.order_by('-uploaded_at').first()
        filename = user_resume.resume.path
        response = FileResponse(open(filename, 'rb'))
        return response
    except UserResume.DoesNotExist:
        raise Http404("No resume found for this user.")


@login_required
@employer_required
@emp_profile_completed
def download_resume_employer(request, uiud):
    try:
        user_resume_uuid = uuid.UUID(uuid)
        user_resume = get_object_or_404(UserResume, pk=user_resume_uuid)
        filename = user_resume.resume.path
        response = FileResponse(open(filename, 'rb'))
        return response
    except ValueError:
        raise Http404("Invalid UUID provided.")
    except UserResume.DoesNotExist:
        raise Http404("No resume found for the provided UUID.")
