from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import SET_NULL
from django.db.models.fields import CharField
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class User(AbstractUser):
    GENDER = [
        ('Male','Male'),
        ('Female','Female'),
    ]

    DIVISIONS = [
        ('Chittagong-চট্টগ্রাম','Chittagong-চট্টগ্রাম'),
        ('Dhaka-ঢাকা','Dhaka-ঢাকা'),
        ('Rajshahi-রাজশাহী','Rajshahi-রাজশাহী'),
        ('Sylhet-সিলেট','Sylhet-সিলেট'),
        ('Mymensingh-ময়মনসিংহ','Mymensingh-ময়মনসিংহ'),
        ('Barisal-বরিশাল','Barisal-বরিশাল'),
        ('Rangpur-রংপুর','Rangpur-রংপুর'),
        ('Khulna-খুলনা','Khulna-খুলনা'),
    ]

    ZILLA = [
        ('Dhaka-ঢাকা','Dhaka-ঢাকা'),
        ('Jessore – যশোর','Jessore – যশোর'),
        ('Dinajpur - দিনাজপুর','Dinajpur - দিনাজপুর'),
        ('Comilla – কুমিল্লা','Comilla – কুমিল্লা'),
        ('Faridpur – ফরিদপুর','Faridpur – ফরিদপুর'),
        ('Bogra – বগুড়া','Bogra – বগুড়া'),
        ('Pabna – পাবনা','Pabna – পাবনা'),
        ('Kushtia – কুষ্টিয়া','Kushtia – কুষ্টিয়া'),
        ('Noakhali - নোয়াখালী','Noakhali - নোয়াখালী'),
    ]

    WORD_NO = [
        ('word-1','word-1'),
        ('word-2','word-2'),
        ('word-3','word-3'),
        ('word-4','word-4'),
        ('word-5','word-5'),
        ('word-6','word-6'),
        ('word-7','word-7'),
        ('word-8','word-8'),
        ('word-9','word-9'),
        ('word-10','word-10'),
        ('word-11','word-11'),
        ('word-12','word-12'),
        ('word-13','word-13'),
        ('word-14','word-14'),
        ('word-15','word-15'),
        ('word-16','word-16'),
        ('word-17','word-17'),
        ('word-18','word-18'),
        ('word-19','word-19'),
        ('word-20','word-20'),
    ]

    BLOD_GROUP = [
        ('A+','A+'),
        ('AB+','AB+'),
        ('A-','A-'),
        ('AB-','AB-'),
        ('B+','B+'),
        ('B-','B-'),
        ('O+','O+'),
        ('O-','O-'),
    ]

    birthcertificateNo = models.CharField(max_length=1000,blank=True, null=True)
    fatherName = models.CharField(max_length =1000,blank=True, null=True)
    motherName = models.CharField(max_length =1000,blank=True, null=True)
    registrationNo = models.CharField(max_length = 1000,blank=True, null=True)
    gender = models.CharField(max_length = 1000,blank=True, null=True,choices=GENDER)
    divisions = models.CharField(max_length = 1000,blank=True, null=True,choices=DIVISIONS)
    zilla = models.CharField(max_length = 1000,blank=True, null=True,choices=ZILLA)
    village = models.CharField(max_length = 1000,blank=True, null=True)
    union = models.CharField(max_length =1000,blank=True, null=True)
    word_no = models.CharField(max_length =1000,blank=True, null=True,choices=WORD_NO)
    holdingNo = models.CharField(max_length =1000,blank=True, null=True)
    sub_block = models.CharField(max_length =1000,blank=True, null=True)
    get_vaccine_from = models.CharField(max_length = 1000,blank=True, null=True)
    profile_pic = models.ImageField(upload_to = 'Profile Pictures',blank=True, null=True)
    blood_group = models.CharField(max_length=1000,blank=True, null=True,choices=BLOD_GROUP)

    is_baby = models.BooleanField(default=False)
    is_ha = models.BooleanField(default=False)

    baby_attached = models.BooleanField(default=False)

    otp = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        if not self.first_name or not self.last_name:
            return self.username
        return self.first_name + ' ' + self.last_name

    @property
    def profile_picURL(self):
        try:
            url = self.profile_pic.url
            return url
        except:
            url = ''
            return url


class BabyAttachedToHealthAssistant(models.Model):
    ha = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True,related_name='ha_iser')
    baby = models.OneToOneField(User,on_delete=models.CASCADE,blank=True, null=True,related_name='baby_user')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.baby.first_name


class ReportIssue(models.Model):
    name = models.CharField(max_length=30,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=30,blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Message(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True,related_name='msg_from_user')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True,related_name='msg_to_user')
    msg = models.TextField(blank=True, null=True)
    sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sender) + ' ' + str(self.receiver)
