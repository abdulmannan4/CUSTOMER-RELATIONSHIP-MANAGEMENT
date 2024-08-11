from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def unauthenticated_user(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('customers:customer_dashboard')  # Ensure this URL exists
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_function

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                group_names = request.user.groups.values_list('name', flat=True)
                if any(role in allowed_roles for role in group_names):
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse('You are not authorized to view this page')
            else:
                return redirect('accounts:login')  # Redirect to login if not authenticated
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            group_names = request.user.groups.values_list('name', flat=True)
            if 'Admin' in group_names:
                return view_func(request, *args, **kwargs)
            elif 'Customer' in group_names:
                return redirect('customers:customer_dashboard')
            else:
                return HttpResponse('You are not authorized to view this page')
        else:
            return redirect('accounts:login')  # Redirect to login if not authenticated
    return wrapper_function