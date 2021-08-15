from django import forms
from django.forms import fields, widgets
from .models import *


class VaccineForm1(forms.ModelForm):
    class Meta:
        model = VaccineCard1
        fields = '__all__'

        widgets = {
            'date1': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'date2': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'date3': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'date4': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'date5': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),    
        }