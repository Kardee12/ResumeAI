from profile import Profile

from django import forms
from django.core.validators import FileExtensionValidator
from .models import UserProfile, Job, ResumeSkills
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

#employer side
class JobForm(forms.ModelForm):
    position = forms.CharField(label = 'Job Position', max_length= 200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Job Position'}))
    description = forms.CharField(label = 'Job Description', widget=forms.Textarea(attrs={'class':'form-control', 'rows' : '3'}))
    pay = forms.CharField(label='Job Pay', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Job Payment Details'}))
    link_to_apply = forms.URLField(label='Link to Apply', max_length=200, required=False, widget=forms.URLInput(attrs={'class':'form-control', 'placeholder': 'Enter Link to Application'}))
    link_to_company = forms.URLField(label='Link to Company', max_length=200,required=False, widget=forms.URLInput(attrs={'class':'form-control', 'placeholder' : 'Enter Link to Company Page'}))
    company_image = forms.ImageField(label = "Company Image", required=False, help_text="Optional Image for the Company")