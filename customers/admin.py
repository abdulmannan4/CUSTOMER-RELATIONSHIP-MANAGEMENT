from django.contrib import admin
from .models import Customer,ExcelFile
from import_export.admin import ImportExportModelAdmin
# Register your models here.
class CustomerAdmin(ImportExportModelAdmin):
    list_display=['id','name','email','phone_number','address']
admin.site.register(Customer,CustomerAdmin)

admin.site.register(ExcelFile)
ExcelFile