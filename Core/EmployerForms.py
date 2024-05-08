from django import forms
from profile import Profile
from .EmployerModel import Job, JobSkills, EmployerProfile, JobType


class JobForm(forms.Form):
    company = forms.CharField(label='Company', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter company name'}))
    position = forms.CharField(label='Job Position', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Job Position'}))
    description = forms.CharField(label='Job Description', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
    pay = forms.CharField(label='Job Pay', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Job Payment Details'}))
    location = forms.CharField(label='Location', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Location Details'}))
    link_to_apply = forms.URLField(label='Link to Apply', max_length=200, required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter Link to Application'}))
    link_to_company = forms.URLField(label='Link to Company', max_length=200, required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter Link to Company Page'}))
    job_type = forms.ChoiceField(choices=JobType.choices, label='Job Type', widget=forms.Select(attrs={'class': 'form-control'}))
    skill_1 = forms.ModelChoiceField(queryset=JobSkills.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    skill_2 = forms.ModelChoiceField(queryset=JobSkills.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    skill_3 = forms.ModelChoiceField(queryset=JobSkills.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    skill_4 = forms.ModelChoiceField(queryset=JobSkills.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    skill_5 = forms.ModelChoiceField(queryset=JobSkills.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    def clean_skills_used(self):
        data = self.cleaned_data['skills_used']
        skill_ids = [s.strip() for s in data.split(',') if s.strip().isdigit()]
        skills = list(JobSkills.objects.filter(id__in=skill_ids))
        if len(skills) != len(skill_ids):
            raise forms.ValidationError("Some skills could not be found. Please enter valid skill IDs.")
        return skills

class EmployerProfileForm(forms.Form):
    company_name = forms.CharField(label = 'Company Name',max_length = 255, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Your Company Name'}))
    position = forms.CharField(label='Position at Company', max_length=120, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Enter Your Job Title'}))
    company_description = forms.CharField(label='Company Description', widget=forms.Textarea(attrs={'class':'form-control', 'rows':4, 'placeholder':'Tell us about your company'}))
    company_website = forms.URLField(label='Company Website', max_length = 200, widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'https://yourcompany.com'}))