# customer/models.py

from django.db import models
from django.conf import settings
class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=False)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.email


class ExcelFile(models.Model):
    file =models.FileField(upload_to="excel")