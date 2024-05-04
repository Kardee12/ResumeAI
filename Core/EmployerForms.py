from django import forms
from .models import  Job, ResumeSkills, EmployerProfile

class JobForm(forms.Form):
    position = forms.CharField(label = 'Job Position', max_length= 200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Job Position'}))
    description = forms.CharField(label = 'Job Description', widget=forms.Textarea(attrs={'class':'form-control', 'rows' : '3'}))
    pay = forms.CharField(label='Job Pay', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Job Payment Details'}))
    link_to_apply = forms.URLField(label='Link to Apply', max_length=200, required=False, widget=forms.URLInput(attrs={'class':'form-control', 'placeholder': 'Enter Link to Application'}))
    link_to_company = forms.URLField(label='Link to Company', max_length=200,required=False, widget=forms.URLInput(attrs={'class':'form-control', 'placeholder' : 'Enter Link to Company Page'}))
    company_image = forms.ImageField(label = "Company Image", required=False, help_text="Optional Image for the Company")
    
    skills_used = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    
    # # used radio select so that they can view the job searcher profile
    # list_of_applicants = forms.RadioSelect(
    #     choices = [],
    #     widget=forms.RadioSelect(),
    #     required=False
    # )

class EmployerProfileForm(forms.Form):
    company_name = forms.CharField(label = 'Company Name',max_length = 255, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Your Company Name'}))
    company_description = forms.CharField(label='Company Description', widget=forms.Textarea(attrs={'class':'form-control', 'rows':4, 'placeholder':'Tell us about your company'}))
    company_website = forms.URLField(label='Company Website', max_length = 200, widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'https://yourcompany.com'}))
    contact_email = forms.EmailField(label = 'Contact Email', max_length = 200, widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'contact@yourcompany.com'}))
    