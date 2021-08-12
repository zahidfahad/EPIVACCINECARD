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
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def admin_profile(request,id):
    pass


@login_required
def baby_profile(request,id):
    user = User.objects.filter(id = id)
    details = User.objects.get(id = id)
    my_health_assistant = BabyAttachedToHealthAssistant.objects.filter(
        baby_id = id, ha__divisions = details.divisions,
        ha__zilla = details.zilla,ha__word_no = details.word_no)
    try:
        report_to = BabyAttachedToHealthAssistant.objects.get(baby_id = id, ha__divisions = details.divisions,
                                                      ha__zilla = details.zilla,ha__word_no = details.word_no)
    except:
        report_to = None

    context = {
        'user': user,
        'details': details,
        'my_health_assistant': my_health_assistant,
        'report_to': report_to,
        'id': id,
    }
    return render(request,'user/baby_profile.html',context)


@login_required
def heath_assistant_profile(request,id):
    user = User.objects.filter(id = id)
    details = User.objects.get(id = id)
    my_area_users_filtering = User.objects.filter(is_baby = True, divisions = details.divisions,
                                            zilla = details.zilla, word_no = details.word_no)
    for i in my_area_users_filtering:
        attached_babies = BabyAttachedToHealthAssistant.objects.filter(baby_id = i.id)
        if not attached_babies:
            BabyAttachedToHealthAssistant.objects.get_or_create(ha_id = id, 
                                                    baby_id = i.id, baby__is_baby = True)


    my_area_users = BabyAttachedToHealthAssistant.objects.filter(ha_id = id, baby__divisions = details.divisions,
                                                        baby__zilla = details.zilla,baby__word_no = details.word_no)
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


@login_required
def edit_profile_baby(request,id):
    if id == request.user.id or request.user.is_superuser or request.user.is_ha:
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
        return render(request,'user/edit_profile_baby.html',context)
    else:
        return redirect('forbidden')


@login_required
def change_pass(request):
    form = PasswordChangeForm(request.user)
    try:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                return redirect('logout')
    except:
        return HttpResponse('Internal Server Error')
    context = {
        'form': form,
    }
    return render(request, 'user/change_password.html', context)


@login_required
def chat(request,id):
    if request.method == 'POST':
        sender = request.user
        msg = request.POST.get('msg')
        Message.objects.create(
            sender = sender,
            receiver_id = id,
            msg = msg
        )
    my_msgs = Message.objects.filter(Q(sender = request.user, receiver_id = id) | 
                                     Q(sender_id = id, receiver = request.user))
    context = {
        'my_msgs': my_msgs,
        'id': id,
    }
    return HttpResponse(context)


def search(request):
    query = request.GET.get('q')
    user = User.objects.filter(Q(username__startswith = query) | Q(registrationNo__startswith = query) |
    Q(email__startswith = query) | Q(first_name__startswith = query) | 
    Q(last_name__startswith = query)|Q(fatherName__startswith = query)|Q(motherName__startswith = query)|
    Q(zilla__startswith = query) | Q(village__startswith = query) | Q(word_no__icontains = query)|
    Q(get_vaccine_from__startswith = query))
    if user:
        context = {
            'user': user,
        }
        return render(request,'user/search_results.html',context)
    else:
        return HttpResponse('No results')
    

@login_required    
def autocomplete(request):
    mylist = []
    query = request.GET.get('term')
    user = User.objects.filter(Q(username__startswith = query) | Q(registrationNo__startswith = query) |
                                                    Q(email__startswith = query) | Q(first_name__startswith = query) | 
                                                    Q(last_name__startswith = query)|Q(fatherName__startswith = query)|Q(motherName__startswith = query)|
                                                    Q(zilla__startswith = query) | Q(village__startswith = query) | Q(word_no__icontains = query)|
                                                    Q(get_vaccine_from__startswith = query))
    if user:
        mylist += [i.first_name for i in user]
    else:
        mylist = ['No user found']
    return JsonResponse(mylist, safe=False)