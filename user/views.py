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
from vaccine.models import VaccineCard1
from vaccine.forms import VaccineForm1
from .decorators import has_perm_baby, user_passes_test, has_perm_admin_ha,has_perm_admin,has_perm_admin_baby, \
                        has_perm_ha,forbidden,REDIRECT_FIELD_NAME
from datetime import datetime


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
        return render(request,'dashboard/dashboard.html')
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
    pass


@login_required
def baby_profile(request,id):
    data = None
    user = User.objects.filter(id = id, is_baby = True)
    details = User.objects.get(id = id, is_baby = True)
    my_health_assistant = BabyAttachedToHealthAssistant.objects.filter(
        baby_id = id, ha__divisions = details.divisions,
        ha__zilla = details.zilla,ha__word_no = details.word_no)
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
    form = VaccineForm1(instance = data)
    if request.method == 'POST':
        form = VaccineForm1(request.POST,instance = data)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.to_user = User.objects.get(id = id)
            instance.by_user = request.user
            instance.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {
        'user': user,
        'details': details,
        'my_health_assistant': my_health_assistant,
        'report_to': report_to,
        'form': form,
        'id': id,
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

    vaccine_done = 30
    context = {
        'user': user,
        'my_area_users': my_area_users,
        'vaccine_done': vaccine_done,
        'reports': reports,
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





















# from django.core.mail import send_mail, BadHeaderError
# from django.contrib.auth.forms import PasswordResetForm
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.encoding import force_bytes
# from django.contrib import messages #import messages


# def password_reset_request(request):
#     if request.method == "POST":
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             associated_users = User.objects.filter(Q(username=username))
#             if associated_users.exists():
#                 for user in associated_users:
#                     c = {
# 					"email":user.email,
# 					'domain':'your-website-name.com',
# 					'site_name': 'Website Name',
# 					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
# 					'token': default_token_generator.make_token(user),
# 					'protocol': 'https',
# 					}

#                     message = client.messages \
#                                 .create(
#                                     body = f"""Hello { user.first_name }. please clink on this link to reset your password 
#                                                {get_current_site(request).domain}
                                    
                                    
#                                     """,
#                                     from_ = '+12397471656',
#                                     to = '+880'+str(user.username)
#                                 )

#     form = PasswordResetForm()
#     context = {
#         'form': form,
#     }
#     return render(request,'user/password_reset.html',context)