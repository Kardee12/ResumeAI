from django import forms
from profile import Profile

from django.core.exceptions import ValidationError

from .EmployerModel import Job, JobSkills, EmployerProfile, JobType


class JobForm(forms.Form):
    position = forms.CharField(label='Job Position', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Job Position'}))
    description = forms.CharField(label='Job Description', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
    pay = forms.IntegerField(label='Job Pay', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Job Payment Details'}))
    location = forms.CharField(label='Location', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Location Details'}))
    link_to_apply = forms.URLField(label='Link to Apply', max_length=200, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter Link to Application'}))
    job_type = forms.ChoiceField(choices=[('Contractor', 'Contractor'), ('Internship', 'Internship'), ('Full-time', 'Full-time'), ('Part-time', 'Part-time')])
    skill_1 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    skill_2 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    skill_3 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    skill_4 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    skill_5 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    def clean(self):
        super().clean()
        skills = [self.cleaned_data.get(f'skill_{i}') for i in range(1, 6)]
        for skill in skills:
            if skill and skill.count(' ') > 1:
                raise ValidationError("Each skill should contain at most one space.")
        return self.cleaned_data

class EmployerProfileForm(forms.Form):
    company_name = forms.CharField(label = 'Company Name',max_length = 255, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Your Company Name'}))
    position = forms.CharField(label='Position at Company', max_length=120, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Enter Your Job Title'}))
    company_role_description = forms.CharField(label='Company Role Description', widget=forms.Textarea(attrs={'class':'form-control', 'rows':4, 'placeholder':'Tell us about your role at your company'}))
    company_website = forms.URLField(label='Company Website', max_length = 200, widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'https://yourcompany.com'}))
    
class EditEmployerProfile(forms.Form):
    model = EmployerProfile
    fields = ['position', 'company_name', 'company_role_description', 'company_website']
    widgets = {
        'position': forms.TextInput(attrs={'class': 'form-control'}),
        'company_name': forms.TextInput(attrs={'class': 'form-control'}),
        'company_role_description': forms.Textarea(attrs={'class': 'form-control'}),
        'company_website': forms.URLInput(attrs={'class': 'form-control'}),
    }
