from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    resume_link = forms.CharField(label='Resume Link', help_text='Please provide a direct link to your resume (e.g., Google Drive link).')
    
    class Meta:
        model = Student
        fields = ['name', 'branch', 'cgpa', 'resume_link']



from django import forms

class SendRequestForm(forms.Form):
    pass
