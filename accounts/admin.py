from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role, UserRole

class UserAdmin(BaseUserAdmin):
    # Define the fields to display in the user detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'tc')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('created_at', 'updated_at')}),
    )

    # Define the fields to display when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'tc', 'password1', 'password2')}
        ),
    )
    
    # Define which fields to display in the list view
    list_display = ('email', 'name', 'tc', 'is_staff', 'is_superuser', 'is_active')
    
    # Define which fields to use for searching
    search_fields = ('email', 'name')
    
    # Define the default ordering
    ordering = ('email',)
    
    # Include groups and permissions
    filter_horizontal = ('groups', 'user_permissions',)

    # Make non-editable fields read-only
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(User, UserAdmin)

# Register the Role and UserRole models if needed
admin.site.register(Role)
admin.site.register(UserRole)
