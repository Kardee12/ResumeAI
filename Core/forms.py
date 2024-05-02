from profile import Profile

from django import forms
from django.core.validators import FileExtensionValidator
from .models import UserProfile
class UserProfileForm(forms.Form):
    location = forms.CharField(label='Location', max_length=255, required=False)
    bio = forms.CharField(label='Professional Bio', widget=forms.Textarea, required=False)
    resume = forms.FileField(
        label='Upload Resume',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])],
        required=True,
        help_text='Accepted formats: PDF, DOC, DOCX'
    )
class EditProfileForm(forms.Form):
    location = forms.CharField(label='Location', max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your location', 'id': 'locationInput'}))
    bio = forms.CharField(label='Professional Bio', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)
    resume = forms.FileField(
        label='Upload Resume',
        required=False,
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])],
        help_text='Accepted formats: PDF, DOC, DOCX',
        widget=forms.FileInput(attrs={'class': 'form-control'}
                               )
    )

