# Django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.transaction import atomic
# Models
from django.contrib.auth.models import User
from users.models import Profile

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request)
            return redirect('home')
        else:
            return render(request, 'usuarios/login.html', {'error': 'Invalid username and password'})

    return render(request, 'usuarios/login.html')

@atomic
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']

        if User.objects.filter(username=username).first(): 
            return render(request, 'usuarios/signup.html', {'error': 'El cuit pertenecen a una cuenta'})

        user = User()
        user.username = username
        user.password = request.POST['password']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()

        profile = Profile()
        profile.user = user
        profile.celular = request.POST['celular']
        profile.save()

    return render(request, 'usuarios/signup.html')