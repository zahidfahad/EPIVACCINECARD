from user.decorators import has_perm_admin_ha
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import REDIRECT_FIELD_NAME, update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *
from .decorators import has_perm_baby, user_passes_test, has_perm_admin_ha,has_perm_admin,has_perm_admin_baby, \
                        has_perm_ha,forbidden,REDIRECT_FIELD_NAME
from datetime import datetime

# Create your views here.
def unique_registrationNo():
    date = datetime.now()
    timestamp = datetime.timestamp(date)
    registrationNo = '#REG' + str(round(timestamp))
    return registrationNo


@login_required
def dashboard(request):
    if request.user.is_superuser:
        return render(request,'dashboard/dashboard.html')
    elif request.user.is_ha:
        return redirect('heath_assistant_profile',id = request.user.id)
    elif request.user.is_baby:
        return redirect('baby_profile',id = request.user.id)

def register(request):
    form = UserCreation()
    if request.method == 'POST':
        form = UserCreation(request.POST,request.FILES)
        is_ha = request.POST.get('is_ha')
        is_baby = request.POST.get('is_baby')

        if is_ha is not None:
            is_ha = True
        else:
            is_ha = False
        
        if is_baby is not None:
            is_baby = True
        else:
            is_baby = False

        if form.is_valid():
            if not is_baby and not is_ha:
                return HttpResponse('Please select a registration type')
            user = form.save(commit=False)
            user.is_ha = is_ha
            user.is_baby = is_baby
            user.registrationNo = unique_registrationNo()
            user.save()
            return redirect('login')
    context = {
        'form': form,
    }
    return render(request,'registration/register.html',context)

@login_required
def visit_profile(request,id):
    user = User.objects.get(id = id)
    if user.is_ha:
        return redirect('heath_assistant_profile', id)
    elif user.is_baby:
        return redirect('baby_profile',id)
    elif user.is_superuser:
        return redirect('admin_profile',id)


@login_required

def heath_assistant_profile(request,id):
    user = User.objects.filter(id = id)
    details = User.objects.get(id = id)
    my_area_users = User.objects.filter(is_baby = True,divisions = details.divisions,
                                            zilla = details.zilla,word_no = details.word_no)
    print(my_area_users)
    context = {
        'user': user,
        'my_area_users': my_area_users,
        'id': id,
    }
    return render(request,'user/ha_profile.html',context)


@login_required
@user_passes_test(has_perm_ha,REDIRECT_FIELD_NAME)
def edit_profile_ha(request,id):
    if id == request.user.id or request.user.is_superuser:
        data = User.objects.get(id=id)
        form = EditProfile(instance=data)
        if request.method == 'POST':
            form = EditProfile(request.POST,request.FILES,instance=data)
            if form.is_valid():
                form.save()
                return redirect('visit_profile', id)
        context = {
            'form': form,
            'data': data,
            'id': id,
        }
        return render(request,'user/edit_profile_ha.html',context)
    else:
        return redirect('forbidden')



