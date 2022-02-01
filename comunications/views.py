#Django
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail

#Models
from users.models import Profile
from organizations.models import Org

@login_required
def comunications_users_view(request):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    users = Profile.objects.all()
    if request.method == 'POST':
        users_id = request.POST.getlist('orgs')
        emails = []
        for u in users_id:
            user = Profile.objects.get(id=u)
            emails.append(user.email)

        subject = f'SOAC: Comunicado de {request.user.first_name}'
        msg = request.POST['msg']
        message = f'''Hola! Te contacto desde SOAC porque {request.user.first_name} {request.user.last_name} te envio el siguiente comunicado:

        {msg}'''

        email_from = settings.EMAIL_HOST_USER
        if msg:
            send_mail(subject, message, email_from, emails)
            return render(request,'comunications/comunication_users.html', {'users': users, 'alert': 'El mensaje fue enviado con exito', 'level': profile_level})
        else:
            return render(request,'comunications/comunication_users.html', {'users': users, 'error': 'No se ha podido enviar el comunicado', 'level': profile_level})

    return render(request,'comunications/comunication_users.html', {'users': users, 'level': profile_level})

@login_required
def comunications_orgs_view(request):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    orgs = Org.objects.all()
    if request.method == 'POST':
        orgs_id = request.POST.getlist('orgs')
        
        emails = [] 
        for u in orgs_id:
            org = Org.objects.get(id=u)
            emails.append(org.email)

        subject = f'SOAC: Comunicado de {request.user.first_name}'
        msg = request.POST['msg']
        message = f'''Hola! Te contacto desde SOAC porque {request.user.first_name} {request.user.last_name} te envio el siguiente comunicado:

        {msg}'''

        email_from = settings.EMAIL_HOST_USER
        if msg:
            send_mail(subject, message, email_from, emails)
            return render(request,'comunications/comunication_orgs.html', {'orgs': orgs, 'alert': 'El mensaje fue enviado con exito', 'level': profile_level})
        else:
            return render(request,'comunications/comunication_orgs.html', {'orgs': orgs, 'error': 'No se ha podido enviar el comunicado', 'level': profile_level})
            
    return render(request,'comunications/comunication_orgs.html', {'orgs': orgs, 'level': profile_level})