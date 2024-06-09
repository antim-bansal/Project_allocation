from django import forms
from .models import CustomUser

class SignupForm(forms.ModelForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, label='Select your role')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@itbhu.ac.in'):
            raise forms.ValidationError("Only email addresses ending with @itbhu.ac.in are allowed.")
        return email