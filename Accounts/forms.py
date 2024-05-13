from django import forms


class SetupForm(forms.Form):
    """
    Form class for user setup.

    Attributes:
        ROLE_CHOICES (list of tuples): Choices for user roles, consisting of tuples with role keys and labels.
        role (ChoiceField): Field to select the user's role, represented as a radio button.
        linkedin_url (URLField): Field to input the user's LinkedIn URL.
    """
    ROLE_CHOICES = [
        ('employer', 'Employer'),
        ('job_searcher', 'Job-Searcher'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)
    linkedin_url = forms.URLField(required=True)
