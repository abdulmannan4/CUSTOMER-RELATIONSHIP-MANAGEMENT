from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django.core.exceptions import ValidationError
import re

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'tc']  # Note 'tc' is still used

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Change the label of 'tc' field
        if 'tc' in self.fields:
            self.fields['tc'].label = "Terms and Conditions"
            # Reorder fields to ensure 'tc' is rendered last
            self.fields = {**{k: self.fields[k] for k in self.fields if k != 'tc'}, 'tc': self.fields['tc']}

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        # Split the name into parts based on spaces
        name_parts = name.split()
        if not all(part.isalpha() for part in name_parts):
            raise ValidationError('Name must contain only alphabetic characters and spaces.')
        return ' '.join(name_parts).strip()  # Join parts back with a single space and strip any extra whitespace

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error('password2', "Passwords do not match.")
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password']
        user.set_password(password)
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('email', css_class='form-control'),
            
            Field('password', css_class='form-control'),
            
            
            Submit('submit', 'LOGIN', css_class='btn btn-primary w-100')
        )

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

class PasswordResetConfirmForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm new password')

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        new_password2 = cleaned_data.get("new_password2")

        if new_password and new_password2 and new_password != new_password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm new password')

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        new_password2 = cleaned_data.get("new_password2")

        if new_password and new_password2 and new_password != new_password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
