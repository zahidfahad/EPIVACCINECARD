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
    path('health_assistant/profile/<int:id>/', heath_assistant_profile, name = 'heath_assistant_profile'),
    path('baby/profile/<int:id>/', baby_profile, name = 'baby_profile'),
    path('visiting/profile/<int:id>/', visit_profile, name = 'visit_profile'),
    path('edit/heath_assistant/profile/<int:id>/', edit_profile_ha, name = 'edit_profile_ha'),
    path('edit/profile/baby/<int:id>/', edit_profile_baby, name = 'edit_profile_baby'),
    path('chat/<int:id>/', chat, name = 'chat'),

    path('forbidden/', forbidden, name = 'forbidden'),
    path('change/password/', change_pass, name = 'change_pass'),
]
