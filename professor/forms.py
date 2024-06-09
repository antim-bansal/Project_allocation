# forms.py in your professor app

from django import forms
from .models import Professor, Project

# class ProfessorForm(forms.ModelForm):
#     class Meta:
#         model = Professor
#         fields = ['name', 'department', 'expertise', 'minimum_cgpa', 'selection_method']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter name'})
#         self.fields['department'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter department'})
#         self.fields['expertise'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter expertise'})
#         self.fields['minimum_cgpa'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter minimum CGPA'})
#         self.fields['selection_method'].widget.attrs.update({'class': 'form-control'})

from django import forms
from .models import Professor, Project

class ProfessorForm(forms.ModelForm):
    is_hod = forms.BooleanField(label='Head of Department', required=False)

    class Meta:
        model = Professor
        fields = ['name', 'department', 'expertise', 'minimum_cgpa', 'selection_method', 'is_hod']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter name'})
        self.fields['department'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter department'})
        self.fields['expertise'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter expertise'})
        self.fields['minimum_cgpa'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter minimum CGPA'})
        self.fields['selection_method'].widget.attrs.update({'class': 'form-control'})

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'max_students']
        
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)