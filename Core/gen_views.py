import uuid

from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404

from Core.models import UserResume
from ResumeAI.Generic.generic_decoraters import emp_profile_completed, employer_required


def download_resume(request):
    """
    View function for downloading user's resume.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: user's resume file for download

    """
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
    """
    View function to download a job searcher's resume by the employer.

    This function allows an employer user to download the resume of a job searcher based on the provided UUID.
    It first validates the UUID format, then retrieves the user resume object using the UUID. If the UUID is
    valid and corresponds to an existing resume, it generates a file response to allow the employer to download
    the resume. If the UUID is invalid or does not correspond to any existing resume, it raises a 404 error.

    Args:
        request (HttpRequest): The HTTP request object.
        uuid (str): The UUID of the user resume to be downloaded.

    Returns:
        FileResponse: File response containing the resume file for download.

    Raises:
        Http404: If the provided UUID is invalid or does not correspond to any existing resume.
    """
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
