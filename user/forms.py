from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import fields, widgets
from .models import *

class UserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','birthcertificateNo','fatherName','motherName','is_baby',
                  'gender','divisions','zilla','village','union','word_no','holdingNo','sub_block','get_vaccine_from',
                  'email','registrationNo','profile_pic'
                ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birthcertificateNo': forms.TextInput(attrs={'class': 'form-control'}),   
            'fatherName': forms.TextInput(attrs={'class': 'form-control'}),
            'motherName': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'divisions': forms.Select(attrs={'class': 'form-control','required': True}),
            'zilla': forms.Select(attrs={'class': 'form-control','required': True}),       
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'union': forms.TextInput(attrs={'class': 'form-control'}),
            'word_no': forms.Select(attrs={'class': 'form-control','required': True}),
            'holdingNo': forms.TextInput(attrs={'class': 'form-control'}),
            'sub_block': forms.Select(attrs={'class': 'form-control','placeholder': 'A-1'}),
            'get_vaccine_from': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class HACreation(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','birthcertificateNo','fatherName','motherName','is_ha',
                  'gender','divisions','zilla','village','union','word_no','sub_block','get_vaccine_from',
                  'email','registrationNo','profile_pic'
                ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control','required': True}),
            'birthcertificateNo': forms.TextInput(attrs={'class': 'form-control'}),   
            'fatherName': forms.TextInput(attrs={'class': 'form-control'}),
            'motherName': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'divisions': forms.Select(attrs={'class': 'form-control','required': True}),
            'zilla': forms.Select(attrs={'class': 'form-control','required': True}),       
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'union': forms.TextInput(attrs={'class': 'form-control'}),
            'word_no': forms.Select(attrs={'class': 'form-control','required': True}),
            'holdingNo': forms.TextInput(attrs={'class': 'form-control'}),
            'sub_block': forms.Select(attrs={'class': 'form-control'}),
            'get_vaccine_from': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class EditProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ['birthcertificateNo','fatherName','motherName','gender','divisions','zilla',
        'village','union','word_no','holdingNo','sub_block','get_vaccine_from','profile_pic',
        'blood_group','first_name','last_name','email']

        widgets = {
            'birthcertificateNo': forms.TextInput(attrs={'class': 'form-control'}),
            'fatherName': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'motherName': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.TextInput(attrs={'class': 'form-control'}),   
            'divisions': forms.Select(attrs={'class': 'form-control'}),
            'motherName': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'zilla': forms.Select(attrs={'class': 'form-control'}),       
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'union': forms.TextInput(attrs={'class': 'form-control'}),
            'word_no': forms.Select(attrs={'class': 'form-control'}),
            'holdingNo': forms.TextInput(attrs={'class': 'form-control'}),
            'sub_block': forms.Select(attrs={'class': 'form-control'}),
            'get_vaccine_from': forms.TextInput(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}), 
            'email': forms.EmailInput(attrs={'class': 'form-control'}), 
        }
