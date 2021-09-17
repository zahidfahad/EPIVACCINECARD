from user.decorators import REDIRECT_FIELD_NAME, has_perm_admin_ha
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render,redirect
from .models import *
from .forms import *

# Create your views here.