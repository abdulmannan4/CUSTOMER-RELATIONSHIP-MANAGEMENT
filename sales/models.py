from django.db import models
from django.conf import settings  # Ensure this import is correct
from customers.models import Customer  # Ensure this import is correct

class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Choices for the stage field
    STAGE_CHOICES = [
        ('Lead', 'Lead'),
        ('Contacted', 'Contacted'),
        ('Qualified', 'Qualified'),
        ('Negotiation', 'Negotiation'),
        ('Won', 'Won'),
        ('Lost', 'Lost'),
    ]
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Sale {self.id} - {self.customer} - {self.amount} - {self.stage}"
