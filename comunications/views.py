#Django
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from soac.settings import EMAIL_HOST_USER

#Models
from users.models import Profile
from organizations.models import Org

@login_required
def comunications_users_view(request):
    ''' Enviar mail a usuarios '''
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

        {msg}
        
        DG Relaciones con la Comunidad
        SS de Gestión Comunal
        '''

        email = EmailMessage(subject, message, EMAIL_HOST_USER, emails)
        email.content_subtype = 'html'

        if request.FILES.get('file') != None:
            file = request.FILES['file']
            email.attach(file.name, file.read(), file.content_type)

        if msg:
            email.send()
            return render(request,'comunications/comunication_users.html', {'users': users, 'alert': 'El mensaje fue enviado con exito', 'level': profile_level})
        else:
            return render(request,'comunications/comunication_users.html', {'users': users, 'error': 'No se ha podido enviar el comunicado', 'level': profile_level})

    return render(request,'comunications/comunication_users.html', {'users': users, 'level': profile_level})

@login_required
def comunications_orgs_view(request):
    ''' Enviar mail a organizaciones '''
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

        {msg}
        
        DG Relaciones con la Comunidad
        SS de Gestión Comunal
        '''

        email = EmailMessage(subject, message, EMAIL_HOST_USER, emails)
        email.content_subtype = 'html'

        file = request.FILES['file']
        email.attach(file.name, file.read(), file.content_type)

        if msg:
            email.send()
            return render(request,'comunications/comunication_orgs.html', {'orgs': orgs, 'alert': 'El mensaje fue enviado con exito', 'level': profile_level})
        else:
            return render(request,'comunications/comunication_orgs.html', {'orgs': orgs, 'error': 'No se ha podido enviar el comunicado', 'level': profile_level})
            
    return render(request,'comunications/comunication_orgs.html', {'orgs': orgs, 'level': profile_level})