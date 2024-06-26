from user.decorators import REDIRECT_FIELD_NAME, has_perm_admin_ha
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render,redirect
from .models import *
from .forms import *
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Sum

# Create your views here.
def render_to_pdf(template,context):
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type="application/pdf")

def ha_vaccine_info_all_count_pdf(request, id):
    v2 = VaccineCard2.objects.filter(by_user_id = id )
    bcg = v2.aggregate(Sum('bcg'))
    for k,v in bcg.items():
        bcg = v
    penta = v2.aggregate(Sum('penta'))
    for k,v in penta.items():
        penta = v
    opv = v2.aggregate(Sum('opv'))
    for k,v in opv.items():
        opv = v
    pcv = v2.aggregate(Sum('pcv'))
    for k,v in pcv.items():
        pcv = v
    ipv = v2.aggregate(Sum('ipv'))
    for k,v in ipv.items():
        ipv = v
    mr = v2.aggregate(Sum('mr'))
    for k,v in mr.items():
        mr = v

    context = {
        'bcg': bcg,
        'penta': penta,
        'pcv': pcv,
        'opv': opv,
        'ipv': ipv,
        'mr': mr,
    }

    template = get_template('user/ha_vaccine_info_all_count_pdf.html')
    pdf = render_to_pdf(template, context)
    if pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        content = "inline; filename=vaccine_count.pdf"
        response['Content-Disposition']=content
        return response
    return HttpResponse("not found")


def pdf_property(request,id):
    v2 = VaccineCard2.objects.get(id=id)
    context = {
        'v2': v2,
        'id':id
    }
    template = get_template('user/pdf.html')
    pdf = render_to_pdf(template, context)
    if pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        content = "inline; filename=card.pdf"
        response['Content-Disposition']=content
        return response
    return HttpResponse("not found")


def render_to_pdf_ha(template,context):
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type="application/pdf")


def pdf_property_ha(request,id):
    v2 = VaccineCard2.objects.get(id=id)
    context = {
        'v2': v2,
        'id':id
    }
    template = get_template('user/ha_pdf.html')
    pdf = render_to_pdf_ha(template, context)
    if pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        content = "inline; filename=card.pdf"
        response['Content-Disposition']=content
        return response
    return HttpResponse("not found")