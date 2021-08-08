from django.http.response import HttpResponse
from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth.decorators import user_passes_test

#redirect url
def forbidden(request):
    return render(request,'user/forbidden.html')
REDIRECT_FIELD_NAME = 'forbidden'


#permissions
def has_perm_admin(user):
    return user.is_superuser

def has_perm_baby(user):
    return not user.is_baby

def has_perm_ha(user):
    return user.is_ha

def has_perm_admin_ha(user):
    return user.is_ha or user.is_superuser

def has_perm_admin_baby(user):
    return user.is_baby or user.is_superuser






