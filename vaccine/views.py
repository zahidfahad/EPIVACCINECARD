from user.decorators import REDIRECT_FIELD_NAME, has_perm_admin_ha
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render,redirect
from .models import *
from .forms import *
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
def render_to_pdf(template,context):
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type="application/pdf")


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