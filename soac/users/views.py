# Django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.transaction import atomic

# Models
from django.contrib.auth.models import User
from users.models import Profile

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password', False);
        print(username, password)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login.html', {'error': 'Error en el cuit o la contraseña. Intente devuelta por favor.'})

    return render(request, 'users/login.html')

@login_required
@atomic
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']        
        password = request.POST['password']
        email = request.POST['email']


        if User.objects.filter(username=username).first(): 
            return render(request, 'users/signup.html', {'error': 'El cuit ya pertenece a una cuenta'})

        user = User.objects.create_user(username, email, password)
        user.username = username
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()

        profile = Profile()
        profile.user = user
        profile.mobile = request.POST['mobile']
        profile.save()

    return render(request, 'users/signup.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')