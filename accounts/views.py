from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model, authenticate, login as auth_login
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from django.conf import settings
from django.urls import reverse
from .decorators import unauthenticated_user
from django.contrib.auth.models import Group

from .forms import UserRegistrationForm, UserLoginForm, PasswordChangeForm, PasswordResetRequestForm, PasswordResetConfirmForm

User = get_user_model()


def index(request):
  return render(request, 'accounts/index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            if User.objects.filter(email=user.email).exists():
                form.add_error('email', 'Email already exists')  # Add error to form
                return render(request, 'accounts/register.html', {'form': form})
            user.is_active = False
           

            # Deactivate account until email is confirmed
            user.save()
            default_group = Group.objects.get(name='Customer')  # Replace with default group name
            user.groups.add(default_group)
            # Generate email verification token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_link = request.build_absolute_uri(f'/verify-email/{uid}/{token}/')

            # Send verification email
            send_mail(
                'Email Verification',
                f'Click the link to verify your email address: {verification_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return redirect('accounts:registration_complete')  # Redirect to registration complete page
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

def verify_email(request, uidb64, token):
    print(f"UID: {uidb64}")
    print(f"Token: {token}")

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(f"User found: {user}")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        print("User not found or invalid UID")

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        print(f"User {user} activated and logged in successfully")
        return redirect('accounts:verification_success')
    else:
        print("Invalid token or user")
        return render(request, 'accounts/verification_failed.html')



def verification_success(request):
    return render(request, 'accounts/verification_success.html')

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                # Redirect based on user group
                if user.groups.filter(name='Admin').exists():
                    return redirect('dashboard:dashboard_admin_dashboard')
                elif user.groups.filter(name='Support').exists():
                    return redirect('support:ticket_list')
                elif user.groups.filter(name='Sales').exists():
                    return redirect('sales:sale_list')
                elif user.groups.filter(name='Customer').exists():
                    return redirect('customers:customer_dashboard')
                else:
                    return redirect('login')  # Redirect to login if no group matches
            else:
                form.add_error(None, "Invalid email or password")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def profile_view(request):
    return render(request, 'accounts/profile.html')


def custom_logout(request):
    logout(request)
    return redirect('accounts:logged_out')  # Redirects to the 'logged_out' page

def logged_out(request):
    return render(request, 'accounts/logged_out.html')
    
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']

            if not request.user.check_password(old_password):
                form.add_error('old_password', 'Old password is incorrect')
            else:
                user = request.user
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                return redirect('customers:user_profile')
    else:
        form = PasswordChangeForm()

    return render(request, 'accounts/change_password.html', {'form': form})

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')
                send_mail(
                    'Password Reset Request',
                    f'Click the link to reset your password: {reset_link}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
            return redirect('accounts:password_reset_done')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'accounts/password_reset_request.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = PasswordResetConfirmForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                user.set_password(new_password)
                user.save()
                return redirect('accounts:password_reset_complete')
        else:
            form = PasswordResetConfirmForm()

        return render(request, 'accounts/password_reset_confirm.html', {'form': form})
    else:
        return redirect('accounts:password_reset_invalid')

def registration_complete(request):
    return render(request, 'accounts/registration_complete.html')
def password_reset_complete(request):
    return render(request, 'accounts/password_reset_complete.html')
def password_reset_done(request):
    return render(request, 'accounts/password_reset_done.html')

def password_reset_invalid(request):
    return render(request, 'accounts/password_reset_invalid.html')
