from django.urls import path
from .views import *

urlpatterns = [
    path('card/<int:id>/', pdf_property, name='pdf_property'),
    path('card/ha/<int:id>/', pdf_property_ha, name='pdf_property_ha'),
    path('vaccine/total/done/<int:id>/', ha_vaccine_info_all_count_pdf, name = 'ha_vaccine_info_all_count_pdf'),
]