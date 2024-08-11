# dashboard/models.py

from django.db import models
from customers.models import Customer  # Assuming Customer model is defined in models/customers.py
from support.models import SupportTicket  # Assuming Support model is defined in models/support.py
from sales.models import Sale  # Assuming Sale model is defined in models/sales.py

class Metrics(models.Model):
    total_customers = models.ForeignKey(Customer, on_delete=models.CASCADE)
    recent_activities = models.ForeignKey(SupportTicket, on_delete=models.CASCADE)
    sales_performance = models.ForeignKey(Sale, on_delete=models.CASCADE)
