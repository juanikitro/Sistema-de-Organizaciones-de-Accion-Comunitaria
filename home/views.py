from datetime import datetime

#Django 
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
    return render(request, 'home/home.html', {'level': profile_level})