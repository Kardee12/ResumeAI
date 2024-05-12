from allauth.account.signals import user_signed_up
from django.dispatch import receiver


@receiver(user_signed_up)
def user_signed_up_handler(request, user, **kwargs):
    user.has_completed_setup = False
    user.save()
