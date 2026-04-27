from django.urls import path
from .views import SignupView, LoginView, logout_view, ProfileView, ProfileUpdateView, ChangePasswordView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/',  auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),  name='password_reset_complete'),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile-update/", ProfileUpdateView.as_view(), name="profile-update"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]