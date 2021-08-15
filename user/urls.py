from django.urls import path
from . views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth import views
from .decorators import forbidden

urlpatterns = [
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),

    path('', dashboard, name = 'dashboard'),
    path('register/', register, name= 'register'),
    path('health_assistant/register/', ha_register, name = 'ha_register'),
    path('health_assistant/profile/<int:id>/', heath_assistant_profile, name = 'heath_assistant_profile'),
    path('baby/profile/<int:id>/', baby_profile, name = 'baby_profile'),
    path('visiting/profile/<int:id>/', visit_profile, name = 'visit_profile'),
    path('edit/heath_assistant/profile/<int:id>/', edit_profile_ha, name = 'edit_profile_ha'),
    path('edit/profile/baby/<int:id>/', edit_profile_baby, name = 'edit_profile_baby'),
    path('chat/<int:id>/', chat, name = 'chat'),
    path('search/', search, name = 'search'),
    path('autocomplete/search/', autocomplete, name = 'autocomplete'),

    path('forbidden/', forbidden, name = 'forbidden'),
    path('change/password/', change_pass, name = 'change_pass'),

    # password
    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="accounts/password_reset.html"),
         name="reset_password"),

    # path('reset_password/', password_reset_request, name = 'password_reset_request'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),

    # not responsive template
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),


    path('reports/', reports, name = 'reports'),
    path('individual/report/<int:id>/', individual_report, name = 'individual_report'),
    path('OneTimePassword/verification/<int:id>/', activate, name = 'activate'),
]
