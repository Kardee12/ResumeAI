from profile import Profile

from django import forms
from django.core.validators import FileExtensionValidator
from .models import UserProfile
class UserProfileForm(forms.Form):
    location = forms.CharField(label='Location', max_length=255, required=False)
    bio = forms.CharField(label='Professional Bio', widget=forms.Textarea, required=False)
    resume = forms.FileField(
        label='Upload Resume',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'txt'])],
        required=True,
        help_text='Accepted formats: PDF, DOC, DOCX, TXT'
    )
class EditProfileForm(forms.Form):
    location = forms.CharField(label='Location', max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your location', 'id': 'locationInput'}))
    bio = forms.CharField(label='Professional Bio', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)
    resume = forms.FileField(
        label='Upload Resume',
        required=False,
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'txt'])],
        help_text='Accepted formats: PDF, DOC, DOCX, TXT',
        widget=forms.FileInput(attrs={'class': 'form-control'}
                               )
    )

class ResumeForm(forms.Form):
    job_title_1 = forms.CharField(max_length=100, required=False)
    company_name_1 = forms.CharField(max_length=100, required=False)
    start_date_1 = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_date_1 = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    job_description_1 = forms.CharField(widget=forms.Textarea, required=False)
    job_title_2 = forms.CharField(max_length=100, required=False)
    company_name_2 = forms.CharField(max_length=100, required=False)
    start_date_2 = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_date_2 = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    job_description_2 = forms.CharField(widget=forms.Textarea, required=False)
    job_title_3 = forms.CharField(max_length=100, required=False)
    company_name_3 = forms.CharField(max_length=100, required=False)
    start_date_3 = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_date_3 = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    job_description_3 = forms.CharField(widget=forms.Textarea, required=False)
    degree = forms.CharField(max_length=100)
    institution_name = forms.CharField(max_length=100)
    education_start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    education_end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    skill_1 = forms.CharField(label='Skill 1', max_length=100, required=False)
    skill_2 = forms.CharField(label='Skill 2', max_length=100, required=False)
    skill_3 = forms.CharField(label='Skill 3', max_length=100, required=False)
    skill_4 = forms.CharField(label='Skill 4', max_length=100, required=False)
    skill_5 = forms.CharField(label='Skill 5', max_length=100, required=False)
    skill_6 = forms.CharField(label='Skill 6', max_length=100, required=False)
    skill_7 = forms.CharField(label='Skill 7', max_length=100, required=False)
    skill_8 = forms.CharField(label='Skill 8', max_length=100, required=False)
    skill_9 = forms.CharField(label='Skill 9', max_length=100, required=False)
    skill_10 = forms.CharField(label='Skill 10', max_length=100, required=False)

    def clean(self):
        cleaned_data = super().clean()
        skills = [cleaned_data.get(f"skill_{i + 1}") for i in range(10) if cleaned_data.get(f"skill_{i + 1}")]
        return cleaned_data