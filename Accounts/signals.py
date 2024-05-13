from allauth.account.signals import user_signed_up
from django.dispatch import receiver


@receiver(user_signed_up)
def user_signed_up_handler(request, user, **kwargs):
    """
    Signal handler for user_signed_up signal.

    Args:
        request: The HTTP request object.
        user: The user object representing the signed-up user.
        **kwargs: Additional keyword arguments passed to the signal handler.

    """
    user.has_completed_setup = False
    user.save()
