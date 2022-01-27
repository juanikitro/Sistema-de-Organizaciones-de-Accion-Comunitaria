from datetime import date, timedelta
#Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime

from pymysql import NULL


#Models
from organizations.models import Org
from history.models import Item
from users.models import Profile


#Forms
from organizations.forms import DocumentForm


#PDF
from django.views.generic import TemplateView
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


#Analisis
@login_required
def analysis_view(request):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    global preactivas
    preactivas = Org.objects.filter(state = 'Preactiva').order_by('-registration_request')
    nothing = preactivas.first()

    return render(request, 'inbox/analysis.html', {'preactivas': preactivas, 'nothing': nothing, 'level': profile_level})


@login_required
def return_pre_view(request, pk):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    selected_org = Org.objects.get(id=pk)
    if request.method == 'POST':
        selected_org.state = 'editar'
        selected_org.doc = ''
        selected_org.msg = request.POST.get('msg')
        selected_org.save()
        return redirect('analysis') 

    return render(request, 'inbox/return_pre.html', {'org': selected_org, 'level': profile_level})


@login_required
def sign_pre_view(request, pk):
    selected_org = Org.objects.get(id=pk)

    selected_org.state = 'A firmar'
    selected_org.save()

    return redirect('analysis')


#Edicion
@login_required
def edit_view(request):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    global editar
    editar = Org.objects.filter(state = 'A editar').order_by('-registration_request')
    nothing = editar.first()

    return render(request, 'inbox/edit.html', {'editar': editar, 'nothing': nothing, 'level': profile_level})


#Firma
@login_required
def sign_view(request):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    global sign
    sign = Org.objects.filter(state = 'A firmar').order_by('-registration_request')
    nothing = sign.first()

    return render(request, 'inbox/sign.html', {'sign': sign, 'nothing': nothing, 'level': profile_level})


@login_required
def return_sign_view(request, pk):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level
    
    selected_org = Org.objects.get(id=pk)
    if request.method == 'POST':
        selected_org.state = 'Preactiva'
        selected_org.msg = request.POST.get('msg')
        selected_org.save()
        return redirect('sign') 

    return render(request, 'inbox/return_sign.html', {'org': selected_org, 'level': profile_level})


@login_required
def signing_view(request, pk):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level
    
    global selected_org
    selected_org = Org.objects.get(id=pk)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance = selected_org)

        if form.is_valid():
            selected_org.state = 'Activa'
            selected_org.roac = 'Si'

            if selected_org.enrolled == None:
                selected_org.enrolled = datetime.now().date()
            else: 
                selected_org.renoved = datetime.now().date()

            selected_org.expiration = date.today() + timedelta(days=730)
            form.save()

            history_item = Item()
            history_item.action = f'Solicitud de registro: {selected_org.name}'
            history_item.by = f'{Profile.objects.get(user_id = user_id).first_name} {Profile.objects.get(user_id = user_id).last_name}'
            history_item.save()

            return redirect('org', selected_org.id)
            
    else:
        form = DocumentForm()

    return render(request, 'inbox/signing.html', {'org': selected_org, 'form': form, 'level': profile_level})


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class Certificate_ROAC(TemplateView):
   def get(self, request, *args, **kwargs):
       today = date.today()        
       expiration = date.today() + timedelta(days=730)
       pdf = render_to_pdf('inbox/certificate.html', {'org': selected_org, 'today': today, 'expiration': expiration})
       return HttpResponse(pdf, content_type='application/pdf')