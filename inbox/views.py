from datetime import date, timedelta
from random import expovariate
#Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings

from pymysql import NULL


#Models
from organizations.models import Org
from organizations.models import Roac_orgs
from history.models import Item
from users.models import Profile


#Forms
from inbox.forms import SignForm


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


#Por vencer
@login_required
def forexpire_view(request):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    a_month_ago = datetime.now().date() + timedelta(days=31)
    forexpire = []

    for org in Org.objects.filter(state = 'Activa'):
        if org.expiration != None:
            if org.expiration.date() < a_month_ago:
                forexpire.append(org) 

    for o in Org.objects.filter(state = 'Activa'):
        if o.expiration.date() < datetime.now().date():
            o.state = 'Vencida'
            o.roac = 'No'
            o.save()

            a_month_ago = datetime.now().date() + timedelta(days=31)

            for org in Org.objects.filter(state = 'Activa'):
                if org.expiration.date() < a_month_ago:
                    if org.expiration_mail == 'No':
                        subject = f'SOAC: Organizacion a punto de expirar'
                        email_from = settings.EMAIL_HOST_USER
                        email = org.email
                        emails = [email]
                        text = f'''\
                            Hola! Te contacto desde SOAC porque se esta a punto de vencer la organizacion: {org}.
                            Podes contactarte con alguien de la Direccion General de Relaciones con la Comunidad para volver a registrarla.
                        '''

                        send_mail(subject, text, email_from, emails)

                        org.expiration_mail = 'Si'
                        org.save()

    return render(request, 'inbox/forexpire.html', {
        'forexpire': forexpire, 'level': profile_level
        })


@login_required
def return_pre_view(request, pk):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    selected_org = Org.objects.get(id=pk)
    if request.method == 'POST':
        selected_org.state = 'A editar'
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


@login_required
def msgregister_request_view(request, pk):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level
    
    selected_org = Org.objects.get(id=pk)
    if request.method == 'POST':
        selected_org.msg = request.POST.get('msg')
        selected_org.save()
        return redirect('register_roac', selected_org.id) 

    return render(request, 'inbox/msgsign.html', {'org': selected_org, 'level': profile_level})


@login_required
def sign_view(request):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    global sign
    sign = Org.objects.filter(state = 'Activa', signed = 'No').order_by('-registration_request')
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
def registering_view(request, pk):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level
    
    global selected_org
    selected_org = Org.objects.get(id=pk)

    if request.method == 'POST':
        form = SignForm(request.POST, request.FILES, instance = selected_org)

        if form.is_valid():
            selected_org.state = 'Activa'
            selected_org.roac = 'Si'

            try:
                Roac_orgs.objects.get(org_id = selected_org.id)
            except:
                roac_number = Roac_orgs()
                roac_number.org = selected_org
                roac_number.save()

            if selected_org.enrolled == None:
                selected_org.enrolled = datetime.now().date()
            else: 
                selected_org.renoved = datetime.now().date()

            selected_org.expiration = date.today() + timedelta(days=730)
            form.save()
            selected_org.save()

            subject = f'SOAC: Organizacion registrada con exito'
            email_from = settings.EMAIL_HOST_USER
            email = selected_org.email
            emails = [email]
            text = f'''\
                Hola! Te contacto desde SOAC porque se registro a {selected_org.name}. 
            Fecha de inscripcion / renovacion: {datetime.now().date()}
            Fecha de expiracion: {selected_org.expiration}
            '''

            send_mail(subject, text, email_from, emails)

            history_item = Item()
            history_item.action = f'Registro de: {selected_org.name}'
            history_item.by = f'{Profile.objects.get(user_id = user_id).first_name} {Profile.objects.get(user_id = user_id).last_name}'
            history_item.save()

            return redirect('org', selected_org.id)
            
    else:
        form = SignForm()

    return render(request, 'inbox/registering.html', {'org': selected_org, 'form': form, 'level': profile_level})


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


@login_required
def signing_view(request, pk):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level
    
    global selected_org
    selected_org = Org.objects.get(id=pk)

    if request.method == 'POST':
        form = SignForm(request.POST, request.FILES, instance = selected_org)

        if form.is_valid():
            selected_org.signed = 'Si'
            form.save()
            selected_org.save()

            history_item = Item()
            history_item.action = f'Firmado de: {selected_org.name}'
            history_item.by = f'{Profile.objects.get(user_id = user_id).first_name} {Profile.objects.get(user_id = user_id).last_name}'
            history_item.save()

            return redirect('org', selected_org.id)
            
    else:
        form = SignForm()

    return render(request, 'inbox/signing.html', {'org': selected_org, 'form': form, 'level': profile_level})