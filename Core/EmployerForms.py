from django import forms
from django.core.exceptions import ValidationError

from .EmployerModel import Job, EmployerProfile


class JobForm(forms.Form):
    """
    Form for creating a new job posting.

    company (CharField): field for entering the name of the company
    position (CharField): field for entering the job position
    description (CharField): field for entering the job description
    pay (IntegerField): field for entering the job pay
    location (CharField): field for entering the job location
    link_to_apply (URLField): field for entering the link to apply for the job
    link_to_company (URLField): field for entering the link to the company's website
    job_type (ChoiceField): A dropdown field for selecting the job type.
    skill_1, skill_2, skill_3, skill_4, skill_5 (ModelChoiceField): Fields for choosing
        up to five skills required for the job.

    Methods:
        clean_skills_used: clean and validate the selected skills by checking their IDs against
            the existing skills in the database.
    """
    position = forms.CharField(label='Job Position', max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Job Position'}))
    description = forms.CharField(label='Job Description',
                                  widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
    pay = forms.IntegerField(label='Job Pay', widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Job Payment Details'}))
    location = forms.CharField(label='Location', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Location Details'}))
    link_to_apply = forms.URLField(label='Link to Apply', max_length=200, widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Link to Application'}))
    job_type = forms.ChoiceField(
        choices=[('Contractor', 'Contractor'), ('Internship', 'Internship'), ('Full-time', 'Full-time'),
                 ('Part-time', 'Part-time')])
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
    company_name = forms.CharField(label='Company Name', max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Your Company Name'}))
    position = forms.CharField(label='Position at Company', max_length=120, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Your Job Title'}))
    company_role_description = forms.CharField(label='Company Role Description', widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell us about your role at your company'}))
    company_website = forms.URLField(label='Company Website', max_length=200, widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'https://yourcompany.com'}))


class EditEmployerProfileForm(forms.ModelForm):
    """
    Form for creating or updating an employer profile.

    Attributes:
        company_name (CharField): field for entering the name of the company
        position (CharField): A field for entering the position at the company
        company_description (CharField): field for entering the company description
        company_website (URLField): field for entering the company website
    """
    class Meta:
        model = EmployerProfile
        fields = ['position', 'company_role_description']
        widgets = {
            'position': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter your position at the company'}),
            'company_role_description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your role at the company'}),
        }


class EditJobForm(forms.ModelForm):
    """
    Form for editing job details.

    This form is used to edit various details of a job posting, including position, description, pay, location, and
    link to apply.

    Attributes:
        position (CharField): Field for the job position.
        description (Textarea): Field for the job description.
        pay (NumberInput): Field for payment details.
        location (CharField): Field for the job location.
        link_to_apply (URLInput): Field for the link to apply.

    """
    class Meta:
        model = Job
        fields = ['position', 'description', 'pay', 'location', 'link_to_apply']
        widgets = {
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Job Position'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter Job Description'}),
            'pay': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Payment Details'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Location'}),
            'link_to_apply': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter Link to Apply'}),
        }
