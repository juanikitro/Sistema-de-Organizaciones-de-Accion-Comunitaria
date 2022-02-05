#Django 
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#Models
from users.models import Profile

@login_required
def home_view(request):
    ''' Chequea el level del usuario nomah '''
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level
    return render(request, 'home/home.html', {'level': profile_level})