from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.index, name='index'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    
    path('verification-success/', views.verification_success, name='verification_success'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset_complete/', views.password_reset_complete, name='password_reset_complete'),
    path('reset-password/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password-reset/done/', views.password_reset_done, name='password_reset_done'),
    path('password-reset/invalid/', views.password_reset_invalid, name='password_reset_invalid'),
    path('registration-complete/', views.registration_complete, name='registration_complete'),
    path('logout/', views.custom_logout, name='logout'),
    path('logged-out/', views.logged_out, name='logged_out'),
]

