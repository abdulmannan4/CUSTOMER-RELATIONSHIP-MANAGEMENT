from django import forms
from support.models import SupportTicket
from accounts.models import User
# Adjust the import based on your project structure
class CreateSupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['customer', 'subject', 'description','status', 'user']
class SupportTicketForm(forms.ModelForm):
    user_email = forms.CharField(max_length=255, disabled=True)  # Display only, not editable

    class Meta:
        model = SupportTicket
        fields = ['subject', 'description', 'user_email']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['user_email'].initial = user.email  # Set the email field to the user's email
            self.instance.user = user
    def clean_description(self):
        # Example of custom validation for description field
        description = self.cleaned_data.get('description')
        if len(description) < 10:
            raise forms.ValidationError("Description must be at least 10 characters long.")
        return description
class SupportTicketFormTeam(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = [ 'status', ]
