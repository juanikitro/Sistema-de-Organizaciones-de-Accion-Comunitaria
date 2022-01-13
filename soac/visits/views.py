#Django & python
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

#Modelos
from visits.models import Visit
from organizations.models import Org
from history.models import Item
from users.models import Profile

    #TODO: Visualizar en las tablas solo las visitaes/eventos/visitas que aun no pasaron

@login_required
def visits_view(request):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    visits = Visit.objects.all().order_by('date')
    orgs = Org.objects.all()
    today = datetime.now().date()
    year = today.year
   
    data = {
       'visit': visits,
       'orgs': orgs,
       'year' : year,
       'level': profile_level,
       'today': datetime.now()
       }

    if request.method == 'POST':
        visit = Visit()
        visit.date = request.POST.get('date')     
        visit.hour = request.POST.get('hour')     
        visit.observation = request.POST.get('observation')     
        visit.org = request.POST.get('org')  
        visit.org_name = Org.objects.get(id = request.POST.get('org')).name
        email = Org.objects.get(id = request.POST.get('org')).email
        visit.save() 
    
        emails  = [email]
        subject = f'SOAC: Visita del dia {visit.date}'
        link = f'http://127.0.0.1:8000/visits/{visit.id}/' #FIXME: Cambiar cuando existan los servers
        email_from = settings.EMAIL_HOST_USER
        message = f'''Hola! Te contacto desde SOAC porque {request.user.first_name} {request.user.last_name} creo una visita. 
        Fecha: {visit.date}
        Hora: {visit.hour}
        Observacion: {visit.observation}
        Podes ver mas sobre esta entrando al siguiente link:
        {link}'''

        send_mail(subject, message, email_from, emails)

        history_item = Item()
        history_item.action = f'Creacion de visita: {visit.org_name}'
        history_item.by = f'{Profile.objects.get(user_id = user_id).first_name} {Profile.objects.get(user_id = user_id).last_name}'
        history_item.save()

        return redirect('visits')

    return render(request,'visits/visits.html', data)

@login_required
def visit_view(request, pk):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    visit = Visit.objects.get(id=pk)
    
    return render(request,'visits/visit.html', {'visit':visit, 'level': profile_level})

@login_required
def visit_delete_view(request, pk):
    user_id = request.user.id
    visit = Visit.objects.get(id=pk)
    email = Org.objects.get(id = visit.org).email

    emails = [email]
    subject = f'SOAC: Eliminacion de visita del dia {visit.date}'
    email_from = settings.EMAIL_HOST_USER
    message = f'''Hola! Te contacto desde SOAC para informarte que la visita del dia: {visit.date} ha sido eliminada.'''

    send_mail(subject, message, email_from, emails)

    history_item = Item()
    history_item.action = f'Eliminiacion de visita: {visit.org_name}'
    history_item.by = f'{Profile.objects.get(user_id = user_id).first_name} {Profile.objects.get(user_id = user_id).last_name}'
    history_item.save()

    visit.delete()

    return redirect('visits')

@login_required
def visit_modify_view(request, pk):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level
    
    visit = Visit.objects.get(id=pk)

    if request.method == 'POST':
        visit.date = request.POST.get('date')     
        visit.hour = request.POST.get('hour')     
        visit.observation = request.POST.get('observation')     
        email = Org.objects.get(id = visit.org).email
        visit.save() 
    
        emails  = [email]
        subject = f'SOAC: Modificacion a la visita del dia {visit.date}'
        link = f'http://127.0.0.1:8000/visits/{visit.id}/' #FIXME: Cambiar cuando existan los servers
        email_from = settings.EMAIL_HOST_USER
        message = f'''Hola! Te contacto desde SOAC porque se ha actualizado la visita del dia {request.POST.get('date')}. 
        Fecha: {request.POST.get('date')}
        Hora: {request.POST.get('hour')}
        Observacion: {request.POST.get('observation')}
        Podes ver mas sobre este entrando al siguiente link:
        {link}'''

        send_mail(subject, message, email_from, emails)

        history_item = Item()
        history_item.action = f'Modificacion de visita: {visit.org_name}'
        history_item.by = f'{Profile.objects.get(user_id = user_id).first_name} {Profile.objects.get(user_id = user_id).last_name}'
        history_item.save()

        return redirect('visit', visit.id)

    return render(request, 'visits/modify_visit.html', {'visit': visit, 'level': profile_level})