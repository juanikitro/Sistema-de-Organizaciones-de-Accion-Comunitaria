from datetime import datetime, timedelta

#Django 
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail

#Models
from users.models import Profile
from organizations.models import Org

@login_required
def home_view(request):
    ''' Chequea el level del usuario
    Y si hay algo para expirar lo expira '''
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    for o in Org.objects.filter(state = 'Activa'):
        if o.expiration.date() == datetime.now().date():
            o.state = 'Suspendida'
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

    return render(request, 'home/home.html', {'level': profile_level})