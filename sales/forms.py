from django import forms
from sales.models import Sale
from customers.models import Customer

#class SaleForm(forms.ModelForm):
 #   class Meta:
  #      model = Sale,Customer
   #    # fields = ['customer', 'amount', 'notes', 'assigned_to']
    #    fields = ['email','phone_number','address', 'amount', 'notes', ]
    
from .models import Sale, Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone_number', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'amount',  'notes'] 
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # Filter the customer choices to only include those belonging to the current user
            self.fields['customer'].queryset = Customer.objects.filter(user=user)



class SaleFormTeam(forms.ModelForm):
    class Meta:
        model = Sale
        fields = [ 'stage']
class CreateSaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = [ 'customer', 'amount', 'notes','stage', 'user']
  