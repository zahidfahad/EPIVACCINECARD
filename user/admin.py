from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(BabyAttachedToHealthAssistant)
admin.site.register(ReportIssue)
admin.site.register(Message)