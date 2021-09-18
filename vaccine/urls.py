from django.urls import path
from .views import *

urlpatterns = [
    path('card/<int:id>/', pdf_property, name='pdf_property'),
]