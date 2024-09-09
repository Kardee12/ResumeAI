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
    
# class EditEmployerProfile(forms.ModelForm):
#     model = EmployerProfile
#     fields = ['position', 'company_name', 'company_role_description', 'company_website']
#     widgets = {
#         'position': forms.TextInput(attrs={'class': 'form-control'}),
#         'company_name': forms.TextInput(attrs={'class': 'form-control'}),
#         'company_role_description': forms.Textarea(attrs={'class': 'form-control'}),
#         'company_website': forms.URLInput(attrs={'class': 'form-control'}),
#     }

class EditEmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile  # Ensure the model is correctly specified
        fields = ['position', 'company_role_description']
        widgets = {
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'company_role_description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    
from django import forms
from .models import Job

class EditJobPosting(forms.ModelForm):
    new_skills = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Enter new skills, separated by commas',
        'class' : 'form-control',
        'rows' : 2
        }))

    class Meta:
        model = Job
        fields = ['position', 'description', 'location', 'pay', 'link_to_apply', 'job_type', 'skills']
        widgets = {
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'pay': forms.NumberInput(attrs={'class': 'form-control'}),
            'link_to_apply': forms.URLInput(attrs={'class': 'form-control'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'skills': forms.CheckboxSelectMultiple(attrs={'class' : 'skills-checkboxes'}),  # Or another suitable widget for multiple selections
        }

    def clean_new_skills(self):
        skills = self.cleaned_data.get('new_skills')
        skill_list = [skill.strip() for skill in skills.split(',') if skill.strip()]
        # Optionally, add further validation here if needed
        return skill_list
