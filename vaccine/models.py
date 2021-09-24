from django.db import models
from django.db.models.fields import CharField
from user.models import User
from django.db.models.deletion import SET_NULL


# Create your models here.
class VaccineCard1(models.Model):
    by_user = models.ForeignKey(User,blank=True, null=True,on_delete=SET_NULL,related_name='ha')
    to_user = models.ForeignKey(User,blank=True, null=True,on_delete=SET_NULL,related_name='baby')

    dose1 = models.TextField(blank=True, null=True)
    date1 = models.DateField(blank=True, null=True)

    dose2 = models.TextField(blank=True, null=True)
    date2 = models.DateField(blank=True, null=True)

    dose3 = models.TextField(blank=True, null=True)
    date3 = models.DateField(blank=True, null=True)

    dose4 = models.TextField(blank=True, null=True)
    date4 = models.DateField(blank=True, null=True)

    dose5 = models.TextField(blank=True, null=True)
    date5 = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.to_user.first_name + self.to_user.last_name



class VaccineCard2(models.Model):
    by_user = models.ForeignKey(User,blank=True, null=True,on_delete=SET_NULL,related_name='health_assistant')
    to_user = models.ForeignKey(User,blank=True, null=True,on_delete=models.CASCADE,related_name='baby_account')

    বিসিজি = models.TextField(blank=True, null=True,default='বিসিজি')
    date_bcg1 = models.CharField(max_length=500,blank=True, null=True)
    date_bcg2 = models.CharField(max_length=500,blank=True, null=True)

    bcg = models.IntegerField(blank=True,null=True)

    পেন্টা = models.TextField(blank=True, null=True,default='পেন্টা (ডিপিটি, হেপ-বি, হিব)')
    date_penta1 = models.CharField(max_length=500,blank=True, null=True)
    date_penta2 = models.CharField(max_length=500,blank=True, null=True)
    date_penta3 = models.CharField(max_length=500,blank=True, null=True)

    penta = models.IntegerField(blank=True,null=True)

    ওপিভি = models.TextField(blank=True, null=True,default='ওপিভি')
    date_opv1 = models.CharField(max_length=500,blank=True, null=True)
    date_opv2 = models.CharField(max_length=500,blank=True, null=True)
    date_opv3 = models.CharField(max_length=500,blank=True, null=True)

    opv = models.IntegerField(blank=True,null=True)

    পিসিভি = models.TextField(blank=True, null=True,default='পিসিভি')
    date_pcv1 = models.CharField(max_length=500,blank=True, null=True)
    date_pcv2 = models.CharField(max_length=500,blank=True, null=True)
    date_pcv3 = models.CharField(max_length=500,blank=True, null=True)

    pcv = models.IntegerField(blank=True,null=True)

    আইপিভি = models.TextField(blank=True, null=True,default='আইপিভি')
    date_ipv1 = models.CharField(max_length=500,blank=True, null=True)
    date_ipv2 = models.CharField(max_length=500,blank=True, null=True)

    ipv = models.IntegerField(blank=True,null=True)

    এমআর  = models.TextField(blank=True, null=True,default='এমআর ')
    date_mr1 = models.CharField(max_length=500,blank=True, null=True)
    date_mr2 = models.CharField(max_length=500,blank=True, null=True)

    mr = models.IntegerField(blank=True,null=True)

    created = models.DateField(auto_now_add=True)