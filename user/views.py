import re
from user.decorators import has_perm_admin_ha
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import REDIRECT_FIELD_NAME, update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.sites.shortcuts import get_current_site
import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *
from vaccine.models import VaccineCard1, VaccineCard2
from vaccine.forms import VaccineForm1
from .decorators import has_perm_baby, user_passes_test, has_perm_admin_ha,has_perm_admin,has_perm_admin_baby, \
                        has_perm_ha,forbidden,REDIRECT_FIELD_NAME
from datetime import datetime
from django.contrib.auth.forms import SetPasswordForm



from twilio.rest import Client
account_sid = 'AC9b8e21ef1e37aa595b7b80e4797a4990'
auth_token = '5c73f7d6f483cb3ed9b264c043258ec8'
client = Client(account_sid, auth_token)

def OTP():
    date = datetime.now()
    timestamp = datetime.timestamp(date)
    otp = round(timestamp)
    return otp


# Create your views here.
def unique_registrationNo():
    date = datetime.now()
    timestamp = datetime.timestamp(date)
    registrationNo = '#REG' + str(round(timestamp))
    return registrationNo


def activate(request,id):
    user = User.objects.get(id = id)
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if int(otp) == user.otp:
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            return HttpResponse('Wrong OTP')
    return render(request,'user/activate.html',{'id': id})


@login_required
def dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_profile',id = request.user.id)
    elif request.user.is_ha:
        return redirect('heath_assistant_profile',id = request.user.id)
    elif request.user.is_baby:
        return redirect('baby_profile',id = request.user.id)


def register(request):
    form = UserCreation()
    if request.method == 'POST':
        form = UserCreation(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            block = user.sub_block
            if '-' in block:
                user.is_baby = True
                user.registrationNo = unique_registrationNo()
                user.is_active = False
                otp = OTP()
                user.otp = otp
                try:
                    client.messages.create(
                                        body = f"Hello { user.first_name }. Yout OTP is { otp }",
                                        from_ = '+12397471656',
                                        to = user.username,
                                    )
                    user.save()
                    return redirect('activate', id = user.id)
                except:
                    return HttpResponse('error sending message. please enter a valid phone number')
            else:
                return HttpResponse('Your Sub block is missing this "-"')
    context = {
        'form': form,
    }
    return render(request,'registration/register.html',context)


def ha_register(request):
    form = HACreation()
    if request.method == 'POST':
        form = HACreation(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            block = user.sub_block
            if '-' in block:
                user.is_ha = True
                user.registrationNo = unique_registrationNo()
                user.is_active = False
                otp = OTP()
                user.otp = otp
                try:
                    client.messages.create(
                                        body = f"Hello { user.first_name }. Yout OTP is { otp }",
                                        from_ = '+12397471656',
                                        to = user.username,
                                    )
                    user.save()
                    return redirect('activate', id = user.id)
                except:
                    return HttpResponse('error sending message. please enter a valid phone number')
            else:
                return HttpResponse('Your Sub block is missing this "-"')
    context = {
        'form': form,
    }
    return render(request,'registration/ha_register.html',context)


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
    user = User.objects.filter(id = id)
    ha = User.objects.filter(is_ha = True)
    baby = User.objects.filter(is_baby = True)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        profile_pic = request.FILES.get('profile_pic')

        User.objects.create(
            username = username,
            email = email,
            first_name = first_name,
            last_name = last_name,
            profile_pic = profile_pic,
            is_superuser = True,
            is_staff = True,
        )
        messages.success(request,'Superuser Created')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {
        'user': user,
        'ha': ha,
        'baby': baby,
        'id': id,
    }
    return render(request,'user/admin_profile.html',context)


@login_required
def baby_profile(request,id):
    data = None
    user = User.objects.filter(id = id, is_baby = True)
    details = User.objects.get(id = id, is_baby = True)
    my_health_assistant = BabyAttachedToHealthAssistant.objects.filter(
        baby_id = id, ha__divisions = details.divisions,
        ha__zilla = details.zilla,ha__word_no = details.word_no)

    date_bcg1 = 0
    date_bcg2 = 0
    date_penta1 = 0
    date_penta2 = 0
    date_penta3 = 0
    date_opv1 = 0
    date_opv2 = 0
    date_opv3 = 0
    date_pcv1 = 0
    date_pcv2 = 0
    date_pcv3 = 0
    date_ipv1 = 0
    date_ipv2 = 0
    date_mr1 = 0
    date_mr2 = 0

    vaccine_2 = VaccineCard2.objects.filter(to_user_id = id)
    for i in vaccine_2:
        if i.date_bcg1:
            date_bcg1 = 1

        if i.date_bcg2:
            date_bcg2 = 1

        if i.date_penta1:
            date_penta1 = 1

        if i.date_penta2:
            date_penta2 = 1

        if i.date_penta3:
            date_penta3 = 1

        if i.date_opv1:
            date_opv1 = 1

        if i.date_opv2:
            date_opv2 = 1

        if i.date_opv3:
            date_opv3 = 1

        if i.date_pcv1:
            date_pcv1 = 1

        if i.date_pcv2:
            date_pcv2 = 1

        if i.date_pcv3:
            date_pcv3 = 1

        if i.date_ipv1:
            date_ipv1 = 1

        if i.date_ipv2:
            date_ipv2 = 1

        if i.date_mr1:
            date_mr1 = 1

        if i.date_mr2:
            date_mr2 = 1          

    bcg = date_bcg1 + date_bcg2
    penta = date_penta1 + date_penta2 + date_penta3
    opv = date_opv1 + date_opv2 + date_opv3
    pcv  = date_pcv1 + date_pcv2 + date_pcv3
    ipv = date_ipv1 + date_ipv2
    mr = date_mr1 + date_mr2

    try:
        report_to = BabyAttachedToHealthAssistant.objects.get(baby_id = id, ha__divisions = details.divisions,
                                                      ha__zilla = details.zilla,ha__word_no = details.word_no)
    except:
        report_to = None

    vaccinecard1 = VaccineCard1.objects.filter(to_user_id = id)
    for i in vaccinecard1:
        try:
            data = VaccineCard1.objects.get(id = i.id)
        except:
            data = None

    try:
        data2 = VaccineCard2.objects.get(to_user_id = id)
    except:
        data2 = None
        
    form = VaccineForm1(instance = data)
    if request.method == 'POST':
        date_bcg1 = request.POST.get('date_bcg1')
        date_bcg2 = request.POST.get('date_bcg2')
        
        date_penta1 = request.POST.get('date_penta1')
        date_penta2 = request.POST.get('date_penta2')
        date_penta3 = request.POST.get('date_penta3')

        date_opv1 = request.POST.get('date_opv1')
        date_opv2 = request.POST.get('date_opv2')
        date_opv3 = request.POST.get('date_opv3')

        date_pcv1 = request.POST.get('date_pcv1')
        date_pcv2 = request.POST.get('date_pcv2')
        date_pcv3 = request.POST.get('date_pcv3')

        date_ipv1 = request.POST.get('date_ipv1')
        date_ipv2 = request.POST.get('date_ipv2')

        date_mr1 = request.POST.get('date_mr1')
        date_mr2 = request.POST.get('date_mr2')

        # checking permission
        if request.user.id == report_to.ha.id or request.user.is_superuser:
            
            if data2 is not None:
                # to update existing
                VaccineCard2.objects.filter(id = data2.id).update(
                                                                by_user = request.user,
                                                                to_user_id = id,
                                                                date_bcg1 = date_bcg1,
                                                                date_bcg2 = date_bcg2,
                                                                date_penta1 = date_penta1,
                                                                date_penta2 = date_penta2,
                                                                date_penta3 = date_penta3,
                                                                date_opv1 = date_opv1,
                                                                date_opv2 = date_opv2,
                                                                date_opv3 = date_opv3,
                                                                date_pcv1 = date_pcv1,
                                                                date_pcv2 = date_pcv2,
                                                                date_pcv3 = date_pcv3,
                                                                date_ipv1 = date_ipv1,
                                                                date_ipv2 = date_ipv2,
                                                                date_mr1 = date_mr1,
                                                                date_mr2 = date_mr2,
                                                            )
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            # to create
            else:
                VaccineCard2.objects.create(
                    by_user = request.user,
                    to_user_id = id,
                    date_bcg1 = date_bcg1,
                    date_bcg2 = date_bcg2,
                    date_penta1 = date_penta1,
                    date_penta2 = date_penta2,
                    date_penta3 = date_penta3,
                    date_opv1 = date_opv1,
                    date_opv2 = date_opv2,
                    date_opv3 = date_opv3,
                    date_pcv1 = date_pcv1,
                    date_pcv2 = date_pcv2,
                    date_pcv3 = date_pcv3,
                    date_ipv1 = date_ipv1,
                    date_ipv2 = date_ipv2,
                    date_mr1 = date_mr1,
                    date_mr2 = date_mr2,
                )
                

            form = VaccineForm1(request.POST,instance = data)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.to_user = User.objects.get(id = id)
                instance.by_user = request.user
                instance.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponse('Not Allowed')

    context = {
        'data2': data2,
        'user': user,
        'details': details,
        'my_health_assistant': my_health_assistant,
        'report_to': report_to,
        'form': form,
        'id': id,
        'bcg': bcg,
        'pcv': pcv,
        'penta': penta,
        'ipv': ipv,
        'mr': mr,
        'opv': opv,
    }
    return render(request,'user/baby_profile.html',context)


@login_required
def heath_assistant_profile(request,id):
    user = User.objects.filter(id = id, is_ha = True)
    details = User.objects.get(id = id, is_ha = True)
    my_area_users_filtering = User.objects.filter(is_baby = True, divisions = details.divisions,
                                            zilla = details.zilla, word_no = details.word_no)
    for i in my_area_users_filtering:
        attached_babies = BabyAttachedToHealthAssistant.objects.filter(baby_id = i.id)
        if not attached_babies:
            BabyAttachedToHealthAssistant.objects.get_or_create(ha_id = id, 
                                                    baby_id = i.id, baby__is_baby = True)


    my_area_users = BabyAttachedToHealthAssistant.objects.filter(ha_id = id, baby__divisions = details.divisions,
                                                        baby__zilla = details.zilla,baby__word_no = details.word_no)
    
    context = {
        'user': user,
        'my_area_users': my_area_users,
        'reports': reports,
        'id': id,
        'bcg': bcg,
        'pcv': pcv,
        'penta': penta,
        'ipv': ipv,
        'mr': mr,
        'opv': opv,
    }
    return render(request,'user/ha_profile.html',context)


@login_required
@user_passes_test(has_perm_admin,REDIRECT_FIELD_NAME)
def edit_profile_admin(request,id):
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
        return render(request,'user/edit_profile_admin.html',context)
    else:
        return redirect('forbidden')



@login_required
@user_passes_test(has_perm_admin_ha,REDIRECT_FIELD_NAME)
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
    if not request.user.is_superuser and not request.user.id == id:
        try:
            attached_ha = BabyAttachedToHealthAssistant.objects.get(baby_id = id)
            print(attached_ha.ha.id)
        except:
            return HttpResponse('This baby has no health assistant and you can not edit this profile')
    if id == request.user.id or request.user.is_superuser or request.user.id == attached_ha.ha.id:
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
        print(request.user.id)
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


@login_required
@user_passes_test(has_perm_ha,REDIRECT_FIELD_NAME)
def reports(request):
    data = []
    reports = Message.objects.filter(receiver = request.user, receiver__is_ha = True).order_by('-sent')
    senders = Message.objects.filter(receiver = request.user).values_list('sender',flat=True).distinct()
    for i in senders:
        users = User.objects.filter(id = i)
        data.append(users)    
    return render(request,'user/reports.html',{
        'reports': reports,
        'data': data
    })


@login_required
def individual_report(request,id):
    reports = Message.objects.filter(receiver = request.user, sender_id = id).order_by('-sent')
    return render(request,'user/reports_individual.html',{
        'reports': reports,
        'id': id
    })


def forgot_password_number(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        try:
            req_user_number = User.objects.get(username = number)
            otp = req_user_number.id
            print(otp)
            try:
                client.messages.create(
                                    body = f"Hello { req_user_number.first_name }. Your OTP is { otp }",
                                    from_ = '+12397471656',
                                    to = req_user_number.username,
                                )
                return redirect('reset_pass', username = req_user_number.username)
            except:
                return HttpResponse('error sending message.')
        except:
            return HttpResponse('Number Not Found')
    return render(request,'user/give_number_for_password_reset.html')


def reset_pass(request,username):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        otp = int(otp)
        try:
            user_otp_exists = User.objects.get(id = otp, username = username)
        except:
            return HttpResponse('Wrong OTP')
        if user_otp_exists:
            password = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password == password2:
                user_otp_exists.set_password(password)
                user_otp_exists.save()
                return redirect('login')
            else:
                return HttpResponse('Two password fields did not match')
    return render(request,'user/password_reset.html')
        