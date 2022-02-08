#Django & python
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

#Modelos
from .models import Event
from activities.models import Activity
from visits.models import Visit
from history.models import Item
from organizations.models import Org
from users.models import Profile

@login_required
def general_calendar_view(request):
    ''' Calendario de eventos / actividades / visitas '''

    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    events = Event.objects.all()
    activities = Activity.objects.all()
    visits = Visit.objects.all()
    today = datetime.now().date()
    year = today.year
   
    data = {
       'event': events,
       'activity': activities,
       'visit': visits,
       'year' : year,
       'level': profile_level
       }

    return render(request,'events/calendar.html', data)

@login_required
def events_view(request):
    ''' Eventos 
    Calendario de eventos
    Creacion de eventos
    Listado de eventos '''
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    events = Event.objects.all().order_by('date')
    orgs = Org.objects.all()
    today = datetime.now().date()
    year = today.year

    data = {
       'event': events,
       'orgs': orgs,
       'year' : year,
       'level': profile_level,
       'today': datetime.now()
       }

    if request.method == 'POST':
        event = Event()
        event.event_name = request.POST.get('event_name')     
        event.date = request.POST.get('date')     
        event.hour = request.POST.get('hour')     
        event.spot = request.POST.get('spot')
        if request.POST.get('allday') == 'on':
            event.allday = 'Si'
        else: 
            event.allday = 'No'
        event.save() 

        history_item = Item()
        history_item.action = f'Creacion de evento: {event.event_name}'
        history_item.by = f'{Profile.objects.get(user_id = user_id).first_name} {Profile.objects.get(user_id = user_id).last_name}'
        history_item.save()

        emails = []
        orgs_id = request.POST.getlist('orgs')
        for u in orgs_id:
            org = Org.objects.get(id=u)
            event.orgs.add(org)
            emails.append(org.email)
                
        if request.POST.get('notify') == 'on':
            subject = f'SOAC: Invitacion al evento "{event.event_name}"'
            link = f'http://172.31.67.157/events/{event.id}/' #FIXME: Cambiar cuando existan los servers
            email_from = settings.EMAIL_HOST_USER
            message = f'''Hola! Te contacto desde SOAC porque {request.user.first_name} {request.user.last_name} te invito al evento "{event.event_name}". 
            Fecha: {event.date}
            Hora: {event.hour}
            Lugar: {event.spot}
            Podes ver mas sobre este entrando al siguiente link:
            {link}'''

            send_mail(subject, message, email_from, emails)

        return redirect('events')

    return render(request,'events/events.html', data)

@login_required
def event_view(request, pk):
    ''' Perfil de evento '''
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    event = Event.objects.get(id=pk)

    orgs = ''
    i = event.orgs.all()
    ids = i.values_list('pk', flat=True)
    for u in ids:
        org = Org.objects.get(id=u)
        orgs_names = (f'{org.name}, ')
        orgs = orgs + orgs_names
    
    return render(request,'events/event.html', {'event':event, 'orgs':orgs, 'level': profile_level})

@login_required
def event_delete_view(request, pk):
    ''' Eliminar evento '''
    user_id = request.user.id
    event = Event.objects.get(id=pk)

    emails = []
    subject = f'SOAC: Eliminacion de evento "{event.event_name}"'
    email_from = settings.EMAIL_HOST_USER
    message = f'''Hola! Te contacto desde SOAC para informarte que el evento "{event.event_name}" ha sido eliminado.'''

    i = event.orgs.all()
    ids = i.values_list('pk', flat=True)
    for u in ids:
        org = Org.objects.get(id=u)
        emails.append(org.email)

    send_mail(subject, message, email_from, emails)

    history_item = Item()
    history_item.action = f'Eliminacion de evento: {event.event_name}'
    history_item.by = f'{Profile.objects.get(user_id = user_id).first_name} {Profile.objects.get(user_id = user_id).last_name}'
    history_item.save()

    event.delete()
    
    return redirect('events')

@login_required
def event_modify_view(request, pk):
    ''' Modificar evento '''
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level
    
    event = Event.objects.get(id=pk)

    if request.method == 'POST':
        event.event_name = request.POST.get('event_name')     
        event.date = request.POST.get('date')     
        event.hour = request.POST.get('hour')     
        event.spot = request.POST.get('spot')     
        event.save()

        history_item = Item()
        history_item.action = f'Modificacion de actividad: {event.event_name}'
        history_item.by = f'{Profile.objects.get(user_id = user_id).first_name} {Profile.objects.get(user_id = user_id).last_name}'
        history_item.save()

        emails = []
        subject = f'SOAC: Modificacion al evento "{event.event_name}"'
        link = f'http://172.31.67.157/events/{event.id}/' #FIXME: Cambiar cuando existan los servers
        email_from = settings.EMAIL_HOST_USER
        message = f'''Hola! Te contacto desde SOAC porque se ha actualizado el evento "{request.POST.get('event_name')}". 
        Fecha: {request.POST.get('date')}
        Hora: {request.POST.get('hour')}
        Lugar: {request.POST.get('spot')}
        Podes ver mas sobre este entrando al siguiente link:
        {link}'''

        i = event.orgs.all()
        ids = i.values_list('pk', flat=True)
        for u in ids:
            org = Org.objects.get(id=u)
            emails.append(org.email)

        send_mail(subject, message, email_from, emails)

        event.save()
        return redirect('event', event.id)

    return render(request, 'events/modify_event.html', {'event': event, 'level': profile_level})