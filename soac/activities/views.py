#Django & python
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

#Modelos
from activities.models import Activity
from organizations.models import Org
from history.models import Item
from users.models import Profile

    #TODO: Visualizar en las tablas solo las actividades/eventos/visitas que aun no pasaron

@login_required
def activities_view(request):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    activities = Activity.objects.all().order_by('date')
    today = datetime.now().date()
    year = today.year
    orgs = Org.objects.all()

    if request.method == 'POST':

        activity = Activity()
        activity.activity_type = request.POST.get('activity_type')     
        activity.date = request.POST.get('date')     
        activity.hour = request.POST.get('hour') 
        if request.POST.get('allday') == 'on':
            activity.allday = 'Si'
        else: 
            activity.allday = 'No'    
        activity.save() 

        orgs_id = request.POST.getlist('orgs')
        emails = []

        history_item = Item()
        history_item.action = f'Creacion de actividad: {activity.activity_type}'
        history_item.by = f'{Profile.objects.get(user_id = user_id).first_name} {Profile.objects.get(user_id = user_id).last_name}'
        history_item.save()

        for u in orgs_id:
            org = Org.objects.get(id=u)
            activity.orgs.add(org)
            emails.append(org.email)

        if request.POST.get('notify') == 'on':
            subject = f'SOAC: Actividad: {activity.activity_type}'
            link = f'http://127.0.0.1:8000/activities/{activity.id}/' #FIXME: Cambiar cuando existan los servers
            email_from = settings.EMAIL_HOST_USER
            message = f'''Hola! Te contacto desde SOAC porque {request.user.first_name} {request.user.last_name} creo la actividad: {activity.activity_type}. 
            Fecha: {activity.date}
            Hora: {activity.hour}
            Tipo: {activity.activity_type}
            Podes ver mas sobre esta entrando al siguiente link:
            {link}'''

            

            send_mail(subject, message, email_from, emails)

        return redirect('activities')

    return render(request,'activities/activities.html', {'today': datetime.now(), 'activity': activities, 'orgs': orgs, 'year': year, 'level': profile_level})

@login_required
def activity_view(request, pk):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level
    
    activity = Activity.objects.get(id=pk)

    orgs = ''
    i = activity.orgs.all()
    ids = i.values_list('pk', flat=True)
    for u in ids:
        org = Org.objects.get(id=u)
        orgs_names = (f'{org.name}, ')
        orgs = orgs + orgs_names
    
    return render(request,'activities/activity.html', {'activity':activity, 'orgs':orgs, 'level': profile_level})

@login_required
def activity_delete_view(request, pk):
    user_id = request.user.id
    activity = Activity.objects.get(id=pk)

    emails = []
    subject = f'SOAC: Eliminacion de actividad "{activity.activity_type}"'
    email_from = settings.EMAIL_HOST_USER
    message = f'''Hola! Te contacto desde SOAC para informarte que la actividad "{activity.activity_type}" ha sido eliminado.'''

    i = activity.orgs.all()
    ids = i.values_list('pk', flat=True)
    for u in ids:
        org = Org.objects.get(id=u)
        emails.append(org.email)

    send_mail(subject, message, email_from, emails)

    history_item = Item()
    history_item.action = f'Eliminacion de actividad: {activity.activity_type}'
    history_item.by = f'{Profile.objects.get(user_id = user_id).first_name} {Profile.objects.get(user_id = user_id).last_name}'
    history_item.save()

    activity.delete()
    
    return redirect('activities')

@login_required
def activity_modify_view(request, pk):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    activity = Activity.objects.get(id=pk)

    if request.method == 'POST':
        activity.activity_type = request.POST.get('activity_type')     
        activity.date = request.POST.get('date')     
        activity.hour = request.POST.get('hour')     
        activity.save()

        emails = []
        subject = f'SOAC: Modificacion al actividad "{activity.activity_type}"'
        link = f'http://127.0.0.1:8000/activities/{activity.id}/' #FIXME: Cambiar cuando existan los servers
        email_from = settings.EMAIL_HOST_USER
        message = f'''Hola! Te contacto desde SOAC porque se ha actualizado la actividad "{request.POST.get('activity_type')}". 
        Fecha: {request.POST.get('date')}
        Hora: {request.POST.get('hour')}
        Podes ver mas sobre esta entrando al siguiente link:
        {link}'''

        i = activity.orgs.all()
        ids = i.values_list('pk', flat=True)
        for u in ids:
            org = Org.objects.get(id=u)
            emails.append(org.email)

        send_mail(subject, message, email_from, emails)

        history_item = Item()
        history_item.action = f'Modificacion de actividad: {activity.activity_type}'
        history_item.by = f'{Profile.objects.get(user_id = user_id).first_name} {Profile.objects.get(user_id = user_id).last_name}'
        history_item.save()

        activity.save()
        return redirect('activity', activity.id)

    return render(request, 'activities/modify_activ.html', {'activity': activity, 'level': profile_level})