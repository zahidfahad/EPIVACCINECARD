from django.db import models
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
