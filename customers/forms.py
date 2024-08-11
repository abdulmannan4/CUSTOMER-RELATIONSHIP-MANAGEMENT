# customers/forms.py

from django import forms
from .models import Customer
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone_number', 'address']  # Adjust fields as needed
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn-primary'))