from django import forms


class SetupForm(forms.Form):
    ROLE_CHOICES = [
        ('employer', 'Employer'),
        ('job_searcher', 'Job-Searcher'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)
    linkedin_url = forms.URLField(required=True)
