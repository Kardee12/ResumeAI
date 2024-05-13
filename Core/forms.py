from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from Core.models import UserProfile


class UserProfileForm(forms.Form):
    """
    Form for user profile creation/update.

    Fields:
        location (CharField): entering the user's location
        bio (CharField): entering the user's professional bio
        resume (FileField): uploading the user's resume

    """
    location = forms.CharField(label='Location', max_length=255, required=False)
    bio = forms.CharField(label='Professional Bio', widget=forms.Textarea, required=False)
    resume = forms.FileField(
        label='Upload Resume',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'txt'])],
        required=True,
        help_text='Accepted formats: PDF, DOC, DOCX, TXT'
    )


class EditProfileForm(forms.ModelForm):
    """
    Form for editing user profile

    Fields:
        location (CharField): entering the user's location
        bio (CharField): entering the user's professional bio
        resume (FileField): uploading the user's resume

    """
    # location = forms.CharField(max_length=100, required=False)
    # summary = forms.CharField(widget=forms.Textarea, required=False)
    resume = forms.FileField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'txt'])],
        help_text="Accepted formats: PDF, DOC, DOCX, TXT"
    )

    class Meta:
        model = UserProfile
        fields = ['location', 'bio']

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume and not resume.name.endswith(('.pdf', '.docx', '.doc', '.txt')):
            raise forms.ValidationError("Invalid file type. Accepted formats: PDF, DOC, DOCX, TXT.")
        return resume


class ResumeForm(forms.Form):
    """
    Form for resume creation/update

    Fields:
        job_title_X (CharField): entering job titles in the user's job history
        company_name_X (CharField): entering company names in the user's job history
        start_date_X (DateField): entering start dates in the user's job history
        end_date_X (DateField): entering end dates in the user's job history
        job_description_X (CharField): entering job descriptions in the user's job history
        degree (CharField): entering the user's degree
        institution_name (CharField): entering the name of the institution
        education_start_date (DateField): entering the start date of education
        education_end_date (DateField): entering the end date of education
        skill_X (CharField): entering skills

    Methods:
        clean: clean the form data and ensure that at least one skill is inputted

    """
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
        if len(skills) != 10:
            raise ValidationError("All 10 skills are required.")
        jobs_required_fields = ['job_title_1', 'company_name_1', 'start_date_1', 'end_date_1', 'job_description_1']
        if not all(cleaned_data.get(field) for field in jobs_required_fields):
            raise ValidationError("At least one complete work experience is required.")
        if cleaned_data['start_date_1'] and cleaned_data['end_date_1']:
            if cleaned_data['start_date_1'] > cleaned_data['end_date_1']:
                raise ValidationError("Start date must be before end date for the job.")
        if cleaned_data['education_start_date'] > cleaned_data['education_end_date']:
            raise ValidationError("Educational start date must be before the end date.")

        return cleaned_data
