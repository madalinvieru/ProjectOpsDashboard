from django import forms
from django.core.exceptions import ValidationError
from .models import User

class SignUpForm(forms.Form):
    firstname = forms.CharField(
        required=False,
        max_length=150
    )

    lastname = forms.CharField(
        required=False,
        max_length=150
    )

    username = forms.CharField(
        required=True,
        min_length=3,
        max_length=150
    )

    email = forms.EmailField(
        required=False
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
        max_length=256
    )

    re_password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
        max_length=256
    )

    role = forms.ChoiceField(
        required=True
    )

    def __init__(
        self,
        *args,      # The form data from request.
        **kwargs    # Extra config arguments.
    ):
        # Find the parameter "user_roles" in the kwargs and extract it. If not provided, default to empty list.
        user_roles = kwargs.pop('user_roles', [])

        # Call the Form's __init__ (this also creates the 'fields' in self).
        super().__init__(*args, **kwargs)

        # Add the provided 'user_roles' to the choices of the 'role' field.
        self.fields['role'].choices = user_roles
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists.')
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError('There already is an account with this email.')
        
        return email
    
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        if password and re_password and password != re_password:
            raise ValidationError('Passwords do not match.')

        return cleaned_data
